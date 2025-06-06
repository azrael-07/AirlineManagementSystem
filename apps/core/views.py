from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.flights.models import Flight, Airport, FlightSeat, SeatType

from apps.bookings.models import AirlineReservation, PassengerSeat, Passenger, Itinerary
from apps.payments.models import CreditCard, ACH, Cash
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse

import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def flight_search(request):
    try:
        # Log the request method and data
        logger.info(f"Request method: {request.method}")
        logger.info(f"POST data: {request.POST}")
        logger.info(f"GET data: {request.GET}")
        # Determine if the request contains search parameters (from either POST or GET)
        if request.method == "POST" or (request.method == "GET" and request.GET.get('departure')):
            # Use POST data if available, otherwise GET data
            data = request.POST if request.method == "POST" else request.GET
            logger.info(f"Using data: {data}")
            # Look up the airports using the provided id (assuming dropdown sends id)
            departure = get_object_or_404(Airport, id=data.get('departure'))
            arrival = get_object_or_404(Airport, id=data.get('arrival'))
            departure_date = data.get('departure_date')

            if not departure_date:
                raise ValueError("Departure date is required")

            departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()

            # Search for outbound flights
            outbound_flights = Flight.objects.filter(
                departure=departure,
                arrival=arrival,
                departure_time__date=departure_date_obj,
                status='Scheduled'
            )

            # Check for roundtrip: if return_date is provided, search for inbound flights
            return_date = data.get('return_date')
            return_flights = []
            if return_date:
                return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
                return_flights = Flight.objects.filter(
                    departure=arrival,  # swapped for return
                    arrival=departure,  # swapped for return
                    departure_time__date=return_date_obj,
                    status='Scheduled'
                )

            # Calculate minimum price and duration for outbound flights (if available)
            if outbound_flights:
                min_price = min(flight.price for flight in outbound_flights)
                min_duration = min(flight.duration for flight in outbound_flights)
            else:
                min_price = None
                min_duration = None

            context = {
                'outbound_flights': outbound_flights,
                'return_flights': return_flights,
                'airports': Airport.objects.all(),
                'min_price': min_price,
                'min_duration': min_duration,
                'form_data': {
                    'departure': departure.id,
                    'arrival': arrival.id,
                    'departure_date': departure_date,
                    'return_date': return_date,
                    'passengers': data.get('passengers'),
                    'payment_method': data.get('payment_method')
                }
            }
            # Log the context being passed to the template
            logger.info(f"Rendering flight_results.html with context: {context}")
            return render(request, 'flight_results.html', context)
        else:
            # No search parameters provided, show the search form
            return render(request, 'flight_search.html', {
                'airports': Airport.objects.all()
            })
    except Exception as e:
        logger.error(f"Error in flight_search view: {str(e)}")
        return render(request, 'flight_search.html', {
            'error': str(e),
            'airports': Airport.objects.all()
        })

def index(request):
    return render(request, 'index.html') 

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("Email:", email)  # Debug output
        print("Password:", password)  # Debug output (be cautious in production!)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            # Role-based redirection (as before)
            if hasattr(user, 'customer'):
                return redirect(reverse('flight_search'))
            elif hasattr(user, 'admin'):
                return redirect(reverse('admin:index'))
            elif hasattr(user, 'pilot'):
                return redirect(reverse('pilot_dashboard'))
            elif hasattr(user, 'frontdeskassit'):
                return redirect(reverse('frontdesk_dashboard'))
            elif hasattr(user, 'crew'):
                return redirect(reverse('crew_dashboard'))
            else:
                return redirect(reverse('index'))
        else:
            print("Authentication failed for:", email)
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def account_info(request): 
    return HttpResponse("Account Info")

@require_http_methods(["GET", "POST"])
def seat_selection(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "skip":
            return redirect("checkout")

        outbound_seat_id = request.POST.get("outbound_seat")
        inbound_seat_id = request.POST.get("inbound_seat")

        if outbound_seat_id:
            request.session["selected_outbound_seat"] = outbound_seat_id
        if inbound_seat_id:
            request.session["selected_inbound_seat"] = inbound_seat_id

        return redirect("checkout")

    # GET: render seat options
    outbound_id = request.GET.get("outbound")
    inbound_id = request.GET.get("inbound")
    tier = request.GET.get("tier", "economy")

    outbound_flight = get_object_or_404(Flight, id=outbound_id)
    inbound_flight = get_object_or_404(Flight, id=inbound_id) if inbound_id else None

    outbound_seats = FlightSeat.objects.filter(flight=outbound_flight, seat_type=tier, is_available=True)
    inbound_seats = FlightSeat.objects.filter(flight=inbound_flight, seat_type=tier, is_available=True) if inbound_flight else []

    context = {
        "outbound_flight": outbound_flight,
        "inbound_flight": inbound_flight,
        "selected_tier": tier,
        "tiers": [choice[0] for choice in SeatType.choices],
        "outbound_seats": outbound_seats,
        "inbound_seats": inbound_seats,
    }
    return render(request, "flight_seats.html", context)

@require_http_methods(["GET", "POST"])
def checkout_view(request):
    if request.method == "POST":
        outbound_seat_id = request.session.get("selected_outbound_seat")
        inbound_seat_id = request.session.get("selected_inbound_seat")

        outbound_seat = get_object_or_404(FlightSeat, id=outbound_seat_id)
        inbound_seat = get_object_or_404(FlightSeat, id=inbound_seat_id) if inbound_seat_id else None

        # Prevent booking for past flights
        now = timezone.now()
        if outbound_seat.flight.departure_time <= now:
            return render(request, "error.html", {"message": "Cannot book a flight that has already departed."})

        if inbound_seat and inbound_seat.flight.departure_time <= now:
            return render(request, "error.html", {"message": "Cannot book a return flight that has already departed."})

        # Create itinerary for current user
        itinerary = Itinerary.objects.create(
            customer=request.user.customer,
            starting_airport=outbound_seat.flight.departure,
            final_airport=inbound_seat.flight.arrival if inbound_seat else outbound_seat.flight.arrival
        )

        reservation = AirlineReservation.objects.create(
            reservationNumber="TEMP123",
            itinerary=itinerary,
            flight=outbound_seat.flight,
        )

        passengers = []
        for i in range(int(request.POST.get("passenger_count"))):
            passport_number = request.POST.get(f"passport_{i}")
            dob = request.POST.get(f"dob_{i}")

            # Check for duplicate passenger on same flight
            if Passenger.objects.filter(passport_number=passport_number, reservation__flight=outbound_seat.flight).exists():
                return render(request, "error.html", {"message": f"Passenger with passport {passport_number} is already booked on this flight."})

            passenger = Passenger.objects.create(
                passport_number=passport_number,
                date_of_birth=dob,
                reservation=reservation
            )
            passengers.append(passenger)

        for passenger in passengers:
            PassengerSeat.objects.create(
                passenger=passenger,
                flight_seat=outbound_seat,
                reservation=reservation
            )
            if inbound_seat:
                PassengerSeat.objects.create(
                    passenger=passenger,
                    flight_seat=inbound_seat,
                    reservation=reservation
                )
        total_price = outbound_seat.price
        outbound_seat.is_available = False
        outbound_seat.save()
        if inbound_seat:
            inbound_seat.is_available = False
            inbound_seat.save()
            total_price += inbound_seat.price 
       
        flight_price = reservation.flight.price
        total_price += flight_price 
        # Simulate payment
        method = request.POST.get("payment_method")
        if method == "credit_card":
            payment = CreditCard.objects.create(
                name_on_card=request.POST.get("card_name"),
                last_four_digits=request.POST.get("card_number")[-4:],
                amount=total_price ,
                reservation=reservation,
                status='approved'
            )
            reservation.payment_credit_card = payment
        elif method == "ach":
            payment = ACH.objects.create(
                bank_name=request.POST.get("bank_name"),
                acc_number_last_four=request.POST.get("account_number")[-4:],
                amount=total_price,
                reservation=reservation,
                status='approved'
            )
            reservation.payment_ach = payment
        elif method == "cash":
            payment = Cash.objects.create(
                cash_tendered=total_price,
                amount=total_price,
                reservation=reservation,
                status='approved'
            )
            reservation.payment_cash = payment

        # Assign the payment_id as the reservation number and confirm
        reservation.reservationNumber = str(payment.payment_id)
        reservation.status = "Confirmed"
        reservation.save()

        return redirect("confirmation")

    # GET: show form
    # return render(request, "checkout.html", {
    #     "outbound_seat_id": request.session.get("selected_outbound_seat"),
    #     "inbound_seat_id": request.session.get("selected_inbound_seat"),
    #     "passenger_count": request.GET.get("passengers", 1)
    # })
    outbound_seat_id = request.session.get("selected_outbound_seat")
    inbound_seat_id = request.session.get("selected_inbound_seat")

    outbound_seat = get_object_or_404(FlightSeat, id=outbound_seat_id)
    inbound_seat = get_object_or_404(FlightSeat, id=inbound_seat_id) if inbound_seat_id else None

    flight = outbound_seat.flight

    selected_seats = {
        "outbound": outbound_seat,
        "inbound": inbound_seat
    }

    return render(request, "checkout.html", {
        "flight": flight,
        "selected_seats": selected_seats,
        "passenger_count": request.GET.get("passengers", 1)
    })

@require_http_methods(["GET"])
def confirmation_view(request):


    # Retrieve the most recent reservation for the current user
    reservations = AirlineReservation.objects.filter(itinerary__customer=request.user.customer).order_by('-id')
    if not reservations.exists():
        return HttpResponse("No reservation found.")

    reservation = reservations.first()
    passengers = Passenger.objects.filter(reservation=reservation)
    seats = PassengerSeat.objects.filter(reservation=reservation).select_related('flight_seat')

    seat_total = sum(seat.flight_seat.price for seat in seats)
    flight_price = reservation.flight.price
    total_price = seat_total + flight_price

    return render(request, "confirmation.html", {
        "reservation": reservation,
        "passengers": passengers,
        "seats": seats,
        "total_price": total_price,
        "seat_total": seat_total,
        "flight_price": flight_price,
    })

@require_http_methods(["GET"])
def pilot_dashboard(request):
    if not hasattr(request.user, 'pilot'):
        return render(request, "error.html", {"message": "Access denied. You are not a pilot."})

    # Show only flights where the pilot is assigned
    pilot = request.user.pilot
    upcoming_flights = Flight.objects.filter(
        pilots=pilot,
        departure_time__gte=datetime.now()
    ).order_by('departure_time')
    return render(request, "pilot_dashboard.html", {"flights": upcoming_flights,
                                                    "pilot": pilot})

@require_http_methods(["GET"])
def crew_dashboard(request):
    if not hasattr(request.user, 'crew'):
        return render(request, "error.html", {"message": "Access denied. You are not crew."})

    # Show all flights today with extra info
    today = timezone.now().date()
    flights = Flight.objects.filter(departure_time__date=today).order_by('departure_time')

    enriched_flights = []
    for flight in flights:
        passenger_count = Passenger.objects.filter(reservation__flight=flight).count()
        pilot_names = flight.pilots.all().values_list('user__name', flat=True)
        enriched_flights.append({
            "flight": flight,
            "passenger_count": passenger_count,
            "pilots": list(pilot_names),
        })

    return render(request, "crew_dashboard.html", {"enriched_flights": enriched_flights})

@require_http_methods(["GET"])
def frontdesk_dashboard(request):
    if not hasattr(request.user, 'frontdeskassit'):
        return render(request, "error.html", {"message": "Access denied. You are not a front desk assistant."})

    # List reservations for upcoming flights
    upcoming_reservations = AirlineReservation.objects.filter(
        flight__departure_time__gte=datetime.now()
    ).select_related("flight", "itinerary", "itinerary__customer").order_by("flight__departure_time")
    return render(request, "frontdesk_dashboard.html", {"reservations": upcoming_reservations})
