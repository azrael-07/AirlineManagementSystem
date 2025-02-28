from django.db import models

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
    aircraft = models.OneToOneField(Aircraft, on_delete=models.CASCADE)
    departure = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    arrival = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    status = models.CharField(max_length=20, choices=FlightStatus.choices, default=FlightStatus.SCHEDULED)

    def __str__(self):
        return f"{self.flight_number} - {self.airline.name}"

    
