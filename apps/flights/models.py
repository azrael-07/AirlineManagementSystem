from django.db import models # type: ignore

# Create your models here.
#flight status Maintainance 
class FlightStatus(models.TextChoices):
    SCHEDULED = "Scheduled", "Scheduled"
    CANCELLED = "Cancelled", "Cancelled"
    COMPLETED = "Completed", "Completed"
    DIVERTED = "Diverted", "Diverted"
    DEPARTED = "Departed", "Departed"
    LANDED = "Landed", "Landed"
    UNKNOWN = "Unknown", "Unknown"
    DELAYED = "Delayed", "Delayed"

class Airline(models.Model):
    name = models.CharField(max_length=200, unique= True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name} is registered with Code {self.code}"

class Aircraft(models.Model):
    model = models.CharField(max_length= 100) 
    airline = models.ForeignKey(Airline , on_delete= models.CASCADE)
    name = models.CharField(max_length=200, unique= True)
    manufacturingYear = models.IntegerField()

    def __str__(self):
        return f"{self.name} Aircraft manufactured in {self.manufacturingYear} for {self.airline.name}"
    
class Airport(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code}) Airport"
    
class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departing_flights")
    arrival = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arriving_flights")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    status = models.CharField(max_length=20, choices=FlightStatus.choices, default=FlightStatus.SCHEDULED)

    def __str__(self):
        return f"{self.flight_number} - {self.airline.name}"



class SeatType(models.TextChoices):
    BUSINESS = 'business', 'business'
    ECONOMY = 'economy', 'economy'
    FIRSTCLASS = 'firstclass', 'firstclass'
    PREMIUMECONOMY = 'premiumeconomy', 'premiumeconomy'


class FlightSeat(models.Model):
    flight= models.ForeignKey(Flight ,on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    seat_type = models.CharField(max_length=20, choices=SeatType.choices, default=SeatType.ECONOMY)
    manufacturingYear = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):  
        return f"{self.seat_number} - {self.seat_type} - f'for { self.flight.flight_number} flying with ' - f'{self.flight.airline.name} is '({'Available' if self.is_available else 'Booked'})"


    

