from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Flight,  FlightSeat
from apps.bookings.models import FlightBaggage

@receiver(post_save, sender=Flight)
def create_flight_baggage(sender, instance, created, **kwargs):
    if created:
        # Calculate total seats for this flight by querying the FlightSeat table.
        total_seats = instance.flightseat_set.count()
        # Compute default capacity: total seats multiplied by 15 kg.
        default_capacity = total_seats * 15
        
        # Create FlightBaggage record only if it doesn't already exist.
        if not hasattr(instance, 'flightbaggage'):
            FlightBaggage.objects.create(flight=instance, total_capacity_kg=default_capacity)