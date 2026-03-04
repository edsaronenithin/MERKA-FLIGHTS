from django import forms
from .models import Contact, Booking

class contactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'mobile', 'message']

class bookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['fname', 'lname','email', 'mobile','cruise','nguest','cabin', 'message']