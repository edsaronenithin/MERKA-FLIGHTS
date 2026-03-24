from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Makes model instances easier to identify in the admin.
    def __str__(self):
        return f"{self.name} - {self.email}"

class Flight(models.Model):
    airline_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.CharField(max_length=50)
    stops = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.airline_name} {self.flight_number} ({self.origin} -> {self.destination})"

class FlightBooking(models.Model):
    # Passenger Information
    passenger_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    passengers = models.IntegerField()
    
    # Travel Details
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    cabin_class = models.CharField(max_length=50)
    
    # Additional Options
    seat_preference = models.CharField(max_length=50, blank=True)
    special_requests = models.TextField(blank=True)
    
    # Meta
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.passenger_name} ({self.origin} to {self.destination})"