from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from apps.bookings.models import AirlineReservation, Passenger, FlightBaggage


def validate_baggage_rules(passenger, weight, flight_baggage=None):
    base_free_limit = 15
    customer = passenger.reservation.itinerary.customer
    travel_count = customer.travel_count
    free_limit = base_free_limit  # might increase
    over_limit = weight - free_limit

    # Rule 0: No need to apply rules if under or equal to 15kg
    if weight <= base_free_limit:
        return True, "Within free baggage limit", 0

    # Rule 1: Special grace for first-time flyers
    if travel_count == 0:
        if flight_baggage:
            est_capacity = flight_baggage.estimate_passenger_capacity()
            if (
                flight_baggage.remaining_capacity > 0.5 * est_capacity or
                est_capacity >= 0.7 * flight_baggage.total_capacity_kg
            ):
                free_limit += 4  # increase allowance
                over_limit = weight - free_limit
                if over_limit <= 0:
                    customer.extra_baggage_allowed += (weight - base_free_limit)
                    customer.save()
                    return True, "4kg grace allowed for first-time flyer", 0
        
    # Rule 2: Frequent flyer with 3+ trips and minimal extra baggage so far
    if travel_count >= 3 and customer.extra_baggage_allowed < 10:
        if over_limit <= 2:
            customer.extra_baggage_allowed += over_limit
            customer.save()
            return True, "Small overage (2kg) waived for loyal passenger", 0

    # Rule 3: Very loyal (5+ trips) → increase free_limit to 20kg
    if travel_count >= 5:
        free_limit = 20
        over_limit = weight - free_limit
        if over_limit <= 10:
            customer.extra_baggage_allowed += over_limit
            customer.save()
            return True, f"{over_limit}kg extra allowed under loyalty benefits", over_limit * 10
        elif weight >= 35:
            return False, "Cannot exceed 35kg even for loyal flyers", 0


    over_limit = weight - free_limit
    if over_limit > 10:
        return False, "Over-limit exceeds maximum allowance of 10kg", 0

    # Final fallback: allow with charge
    return True, f"{over_limit}kg over limit. Extra fee applies", over_limit * 10

# Create your views here.
@require_http_methods(["GET", "POST"])
def checkin_start_view(request):
    message = None
    if request.method == "POST":
        passport = request.POST.get("passport")
        reservation_number = request.POST.get("reservation_number")

        try:
            reservation = AirlineReservation.objects.get(id=reservation_number)
            passenger = Passenger.objects.get(reservation=reservation, passport_number=passport)
            request.session["checkin_passenger_id"] = passenger.id
            return redirect("checkin_baggage")
        except (AirlineReservation.DoesNotExist, Passenger.DoesNotExist):
            message = "No matching reservation/passport found. Please try again or call an agent."

    return render(request, "checkin_start.html", {"message": message})

@require_http_methods(["GET", "POST"])
def checkin_baggage_view(request):
    passenger_id = request.session.get("checkin_passenger_id")
    if not passenger_id:
        return redirect("checkin_start")

    passenger = get_object_or_404(Passenger, id=passenger_id)
    message = None
    extra_fee = 0

    if request.method == "POST":
        try:
            baggage_weight = float(request.POST.get("baggage_weight"))
        except (TypeError, ValueError):
            message = "Please enter a valid baggage weight."
            return render(request, "checkin_baggage.html", {
                "passenger": passenger,
                "message": message,
            })

        is_valid, message, extra_fee = validate_baggage_rules(passenger, baggage_weight)

        if is_valid:
            passenger.baggage_weight = baggage_weight
            passenger.save()
            request.session["extra_fee"] = extra_fee
            return redirect("checkin_payment" if extra_fee > 0 else "checkin_complete")

    return render(request, "checkin_baggage.html", {
        "passenger": passenger,
        "message": message,
        "extra_fee": extra_fee
    })


@require_http_methods(["GET", "POST"])
def checkin_payment_view(request):
    passenger_id = request.session.get("checkin_passenger_id")
    extra_fee = request.session.get("extra_fee", 0)
    payment = None

    if not passenger_id or extra_fee <= 0:
        return redirect("checkin_baggage")

    passenger = get_object_or_404(Passenger, id=passenger_id)

    if request.method == "POST":
        method = request.POST.get("payment_method")
        reservation = passenger.reservation

        if reservation.payment_credit_card:
            payment = reservation.payment_credit_card
        elif reservation.payment_ach:
            payment = reservation.payment_ach
        elif reservation.payment_cash:
            payment = reservation.payment_cash

        if payment:
            payment.amount += extra_fee
            payment.save()

        request.session["checkin_paid"] = True
        return redirect("checkin_complete")

    reservation = passenger.reservation
    return render(request, "checkin_payment.html", {
        "passenger": passenger,
        "extra_fee": extra_fee,
        "reservation": reservation
    })

@require_http_methods(["GET"])
def checkin_complete_view(request):
    passenger_id = request.session.get("checkin_passenger_id")
    if not passenger_id:
        return redirect("checkin_start")

    passenger = get_object_or_404(Passenger, id=passenger_id)
    reservation = passenger.reservation
    flight = reservation.flight
    seats = passenger.passengerseat_set.all()

    # Update FlightBaggage record for this flight if not already updated for this reservation
    if not request.session.get("baggage_updated"):
       
        try:
            flight_baggage = FlightBaggage.objects.get(flight=flight)
            # Calculate the total baggage weight for all passengers in this reservation

            total_baggage = sum(
            p.baggage_weight for p in Passenger.objects.filter(reservation=reservation) if p.baggage_weight
            )
            flight_baggage.used_capacity_kg += total_baggage
            flight_baggage.save()
            request.session["baggage_updated"] = True
            
            customer = passenger.reservation.itinerary.customer
            customer.travel_count += 1
            customer.save()
        except FlightBaggage.DoesNotExist:
            # Optionally, log an error or create a new record if needed
            pass

    return render(request, "checkin_complete.html", {
        "passenger": passenger,
        "reservation": reservation,
        "flight": flight,
        "seats": seats,
        "baggage_weight": passenger.baggage_weight,
        "extra_fee": request.session.get("extra_fee", 0),
    })