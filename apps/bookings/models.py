from django.db import models

# Create your models here.

    
class ReservationStatus(models.TextChoices):
    CONFIRMED = 'Confirmed', 'Confirmed' 
    CANCELLED = 'Cancelled', 'Cancelled' # due to payment Failure
    # Below two status for the admin Purpose and Refund Process 
    CANCELLED_BY_CUSTOMER = 'Cancelled by customer', 'Cancelled by customer' 
    CANCELLED_BY_AIRLINE = 'Cancelled by airline', 'Cancelled by airline' 
    PENDING = 'Pending', 'Pending'
        
class Itinerary(models.Model):
    customer = models.ForeignKey('authentication.Customer' , on_delete= models.CASCADE , related_name='itineraries')
    starting_airport = models.ForeignKey('flights.Airport', on_delete=models.CASCADE, related_name='departing_itineraries')
    final_airport = models.ForeignKey('flights.Airport', on_delete=models.CASCADE, related_name='arriving_itineraries')
    creationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Itinerary is from {self.starting_airport} - to {self.final_airport} for {self.customer.name} customer with {self.customer.frequentFlyingNumber} frequent flying number"

class AirlineReservation(models.Model):
    reservationNumber = models.CharField(max_length= 100)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='reservations')
    flight = models.ForeignKey('flights.Flight', on_delete=models.CASCADE, related_name='reservations')
    seat_map = models.ManyToManyField('flights.FlightSeat', through='PassengerSeat')
    status = models.CharField(max_length=30, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)

    def __str__(self):
        return f"Reservation {self.reservation_number} for {self.itinerary.customer.name} - {self.flight.flight_number}"


class Passenger(models.Model):
    passport_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    reservation = models.ForeignKey(AirlineReservation, on_delete=models.CASCADE, related_name="passengers")

    def __str__(self):
        return f"Passenger {self.passport_number} - Reservation {self.reservation.reservationNumber}"
    
class PassengerSeat(models.Model):
    passenger = models.ForeignKey("bookings.Passenger", on_delete=models.CASCADE)
    flight_seat = models.ForeignKey("flights.FlightSeat", on_delete=models.CASCADE)
    reservation = models.ForeignKey("bookings.AirlineReservation", on_delete=models.CASCADE)

    def __str__(self):
        return f"Seat {self.flight_seat.seat_number} assigned to {self.passenger}"