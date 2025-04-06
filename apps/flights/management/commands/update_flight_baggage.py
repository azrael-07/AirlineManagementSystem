from django.core.management.base import BaseCommand
from apps.flights.models import Flight
from apps.bookings.models import FlightBaggage

class Command(BaseCommand):
    help = "Update FlightBaggage records with default capacity based on total seats * 15."

    def handle(self, *args, **options):
        flights = Flight.objects.all()
        for flight in flights:
            total_seats = flight.flightseat_set.count()
            # Use a fallback value (150 kg) if no seats are found
            default_capacity = total_seats * 15 if total_seats > 0 else 150  
            fb, created = FlightBaggage.objects.get_or_create(
            flight=flight,
            defaults={'total_capacity_kg': default_capacity}
            )
            if not created:
                fb.total_capacity_kg = default_capacity
                fb.save()
            status = "Created" if created else "Updated"
            self.stdout.write(f"{status} FlightBaggage for Flight {flight.flight_number} with capacity {default_capacity} kg.")