from django.contrib import admin
from .models import Itinerary, AirlineReservation, Passenger, PassengerSeat, ReservationStatus

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'starting_airport', 'final_airport', 'creationDate')
    search_fields = ('customer__name', 'starting_airport__name', 'final_airport__name')

@admin.register(AirlineReservation)
class AirlineReservationAdmin(admin.ModelAdmin):
    list_display = ('reservationNumber', 'itinerary', 'flight', 'status')
    search_fields = ('reservationNumber', 'flight__flight_number')
    list_filter = ('status',)

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('passport_number', 'date_of_birth', 'reservation')
    search_fields = ('passport_number', 'reservation__reservationNumber')

@admin.register(PassengerSeat)
class PassengerSeatAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'flight_seat', 'reservation')
    search_fields = ('passenger__passport_number', 'flight_seat__seat_number')

