from django.contrib import admin
from .models import Flight, FlightSeat, Airport, Airline, Aircraft

admin.site.register(Airline)
admin.site.register(Aircraft)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(FlightSeat)
