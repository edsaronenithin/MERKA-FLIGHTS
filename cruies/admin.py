from django.contrib import admin
from .models import Contact, Flight, FlightBooking

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'submitted_at')
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('submitted_at',)
    readonly_fields = ('submitted_at',)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('airline_name', 'flight_number', 'origin', 'destination', 'departure_time', 'price')
    search_fields = ('airline_name', 'flight_number', 'origin', 'destination')
    list_filter = ('origin', 'destination', 'search_date')

@admin.register(FlightBooking)
class FlightBookingAdmin(admin.ModelAdmin):
    list_display = ('passenger_name', 'email', 'origin', 'destination', 'departure_date', 'booking_date')
    search_fields = ('passenger_name', 'email', 'phone_number', 'origin', 'destination')
    list_filter = ('departure_date', 'cabin_class', 'booking_date')
