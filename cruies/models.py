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
    
class Booking(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=50)
    cruise = models.CharField(max_length=100)
    nguest = models.CharField(max_length=10)
    cabin = models.CharField(max_length=100)
    message = models.TextField()
    Booking_at = models.DateTimeField(auto_now_add=True)


    # Makes model instances easier to identify in the admin.
    def __str__(self):
        return f"{self.fname} - {self.email}"