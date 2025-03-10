from django.db import models

# Create your models here.
class Itinerary(models.Model):
    customer = models.ForeignKey('authentication.Customer' , on_delete= models.CASCADE , related_name='itineraries')
    starting_airport = models.ForeignKey('flights.Airport', on_delete=models.CASCADE, related_name='departing_itineraries')
    final_airport = models.ForeignKey('flights.Airport', on_delete=models.CASCADE, related_name='arriving_itineraries')
    creationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Itinerary is from {self.starting_airport} - to {self.final_airport} for {self.customer.name} customer with {self.customer.frequentFlyingNumber} frequent flying number"
