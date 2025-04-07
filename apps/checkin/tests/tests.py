from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from apps.authentication.models import Customer
from apps.flights.models import Airline, Airport, Aircraft, Flight, FlightSeat
from apps.bookings.models import Itinerary, AirlineReservation, Passenger
from django.contrib.auth import get_user_model

User = get_user_model()

class CheckinFlowTestCase(TestCase):
    def setUp(self):
        # Create test user and customer
        self.user = User.objects.create_user(email="customer@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            name="Test Customer",
            address1="123 Test Street",
            pinCode=12345,
            phone="1234567890"
        )

        # Create airline and aircraft
        self.airline = Airline.objects.create(name="Test Airline", code="TA")
        self.aircraft = Aircraft.objects.create(
            model="A320",
            name="TestJet",
            manufacturingYear=2020,
            airline=self.airline
        )

        # Create airports
        self.dep_airport = Airport.objects.create(name="Departure Airport", code="DEP")
        self.arr_airport = Airport.objects.create(name="Arrival Airport", code="ARR")

        # Create flight
        self.flight = Flight.objects.create(
            flight_number="TA101",
            departure=self.dep_airport,
            arrival=self.arr_airport,
            airline=self.airline,
            aircraft=self.aircraft,
            price=199.99,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=2),
            duration=120,
            status="Scheduled"
        )

        # Create flight seat
        self.flight_seat = FlightSeat.objects.create(
            flight=self.flight,
            seat_number="A1",
            seat_type="economy",
            manufacturingYear=2020,
            price=20.00,
            is_available=True
        )

        # Create itinerary and reservation
        self.itinerary = Itinerary.objects.create(
            customer=self.customer,
            starting_airport=self.dep_airport,
            final_airport=self.arr_airport
        )

        self.reservation = AirlineReservation.objects.create(
            reservationNumber="R123",
            itinerary=self.itinerary,
            flight=self.flight
        )

        # Create passenger
        self.passenger = Passenger.objects.create(
            passport_number="P1234567",
            date_of_birth="1995-06-01",
            reservation=self.reservation
        )

        self.client = Client()
    
    def test_checkin_start_valid(self):
        """
        Test that providing a valid reservation number and passport sets the checkin_passenger_id
        in session and redirects to the baggage check-in view.
        """
        url = reverse("checkin_start")
        response = self.client.post(url, {
            "reservation_number": str(self.reservation.id),
            "passport": "P1234567"
        })
        # Expect redirection to the baggage view
        self.assertRedirects(response, reverse("checkin_baggage"))
        # Check that the session variable is set correctly
        session = self.client.session
        self.assertEqual(session.get("checkin_passenger_id"), self.passenger.id)
def test_checkin_baggage_valid_weight(self):
    self.client.session["checkin_passenger_id"] = self.passenger.id
    self.client.session.save()

    response = self.client.post(reverse("checkin_baggage"), {
        "baggage_weight": "17"
    })

    self.passenger.refresh_from_db()
    self.assertEqual(self.passenger.baggage_weight, 17)
    # Extra fee should be calculated (17kg - 15kg = 2kg → $20 if new flyer)
    self.assertEqual(self.client.session["extra_fee"], 20)
    self.assertRedirects(response, reverse("checkin_payment"))

def test_checkin_baggage_invalid_input(self):
    self.client.session["checkin_passenger_id"] = self.passenger.id
    self.client.session.save()

    response = self.client.post(reverse("checkin_baggage"), {
        "baggage_weight": "abc"  # Invalid input
    })

    self.assertContains(response, "Please enter a valid baggage weight.")
    self.passenger.refresh_from_db()
    self.assertEqual(self.passenger.baggage_weight, 0)  # Default value unchanged

def test_checkin_payment_updates_payment(self):
    self.client.session["checkin_passenger_id"] = self.passenger.id
    self.client.session["extra_fee"] = 25
    self.client.session.save()

    # Simulate payment record (e.g., credit card)
    from apps.payments.models import CreditCard
    card = CreditCard.objects.create(
        name_on_card="Test",
        last_four_digits=1234,
        reservation=self.reservation,
        amount=100,
        status="approved"
    )

    response = self.client.post(reverse("checkin_payment"), {
        "payment_method": "credit_card"
    })

    card.refresh_from_db()
    self.assertEqual(card.amount, 125)  # Updated with extra_fee
    self.assertRedirects(response, reverse("checkin_complete"))

def test_checkin_complete_updates_flight_baggage(self):
    from apps.bookings.models import PassengerSeat
    from apps.flights.models import FlightBaggage

    # Create FlightBaggage record manually
    flight_baggage = FlightBaggage.objects.create(
        flight=self.flight,
        total_capacity_kg=300,
        used_capacity_kg=0
    )

    # Simulate check-in baggage weight and passenger seat
    self.passenger.baggage_weight = 20
    self.passenger.save()
    PassengerSeat.objects.create(
        passenger=self.passenger,
        flight_seat=self.flight_seat,
        reservation=self.reservation
    )

    # Prepare session
    session = self.client.session
    session["checkin_passenger_id"] = self.passenger.id
    session["extra_fee"] = 50
    session.save()

    # Call the complete view
    response = self.client.get(reverse("checkin_complete"))
    self.assertEqual(response.status_code, 200)

    # Check baggage capacity is updated
    flight_baggage.refresh_from_db()
    self.assertEqual(flight_baggage.used_capacity_kg, 20)

    # Check rendered content includes flight + baggage info
    self.assertContains(response, self.flight.flight_number)
    self.assertContains(response, "20")  # baggage weight
    self.assertContains(response, "50")  # extra fee

    # You can add additional test methods here for checkin_baggage_view, checkin_payment_view, etc.