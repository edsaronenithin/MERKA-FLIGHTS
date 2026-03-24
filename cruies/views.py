from django.shortcuts import render, redirect
from .forms import contactForm
from .models import Contact, Flight, FlightBooking
from django.utils import timezone
import datetime
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User

def index(request):
    form = contactForm()
    return render(request, 'index.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = contactForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            mobile = form.cleaned_data.get('mobile')
            message = form.cleaned_data.get('message')

            # Save to DB
            form.save()

            # ================================
            # 1️⃣ Email to ADMIN
            # ================================
            admin_subject = f"New Contact Inquiry from {name}"
            admin_message = f"""
Dear Admin,

A new contact inquiry has been received through the Merka Cruises website. Please review the details below:

Contact Information:
--------------------------------------------------
Name:    {name}
Email:   {email}
Phone:   {mobile}

Message:
--------------------------------------------------
{message}

Best Regards,
Merka Cruises Automated System
"""

            try:
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['merkaflight@gmail.com'],  # change this
                    fail_silently=False,
                )
            except Exception as e:
                print("Admin email error:", e)

            # ================================
            # 2️⃣ Auto Reply to USER
            # ================================
            user_subject = "Welcome to Merka Cruises - We've Received Your Message 🚢"
            user_message = f"""
Dear {name},

Warm greetings from Merka Cruises!

Thank you for reaching out to us. We have successfully received your message and one of our dedicated team members will get back to you shortly to assist you further.

We appreciate your interest in Merka Cruises and look forward to speaking with you.

Warm Regards,
The Merka Cruises Customer Care Team
"""

            try:
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print("User email error:", e)

            # Success response
            return render(request, 'index.html', {
                'form': contactForm(),
                'success': True,
                'name': name
            })

    else:
        form = contactForm()

    return render(request, 'index.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        if user is not None:
            auth_login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('/admin/')
            return redirect('index') # redirect to homepage on successful login
        else:
            return render(request, 'components/login.html', {'error': 'Invalid username or password.'})
            
    return render(request, 'components/login.html')

def user_signup(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        email = request.POST.get('email')
        p = request.POST.get('password')
        p2 = request.POST.get('confirm_password')
        
        if p != p2:
            return render(request, 'components/signup.html', {'error': 'Passwords do not match.'})
            
        if User.objects.filter(username=u).exists():
            return render(request, 'components/signup.html', {'error': 'Username already exists.'})
            
        user = User.objects.create_user(username=u, email=email, password=p)
        user.save()
        return redirect('login') 
        
    return render(request, 'components/signup.html')

def mock_flight_api(origin, destination, date_str):
    airlines = ['Emirates', 'Singapore Airlines', 'Air India', 'Thai Airways', 'Qatar Airways', 'Lufthansa', 'British Airways']
    
    try:
        dep_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        dep_date = timezone.now().date()
        
    results = []
    
    for i in range(random.randint(3, 8)):
        airline = random.choice(airlines)
        flight_num = f"{airline[:2].upper()}{random.randint(100, 999)}"
        
        hour = random.randint(0, 23)
        minute = random.choice([0, 15, 30, 45])
        departure_time = timezone.make_aware(datetime.datetime.combine(dep_date, datetime.time(hour, minute)))
        
        dur_hours = random.randint(2, 12)
        dur_mins = random.choice([0, 10, 20, 30, 40, 50])
        duration_str = f"{dur_hours}h {dur_mins}m"
        
        arrival_time = departure_time + datetime.timedelta(hours=dur_hours, minutes=dur_mins)
        
        stops = random.choice(['Direct', '1 Stop', '1 Stop', '2 Stops'])
        price = random.randint(5000, 65000)
        
        flight = Flight.objects.create(
            airline_name=airline,
            flight_number=flight_num,
            origin=origin.upper(),
            destination=destination.upper(),
            departure_time=departure_time,
            arrival_time=arrival_time,
            duration=duration_str,
            stops=stops,
            price=price
        )
        results.append(flight)
        
    return results

def flights(request):
    origin = request.GET.get('origin', '').strip()
    destination = request.GET.get('destination', '').strip()
    departure_date = request.GET.get('departure_date', '')
    
    flights_data = []
    query = False
    
    if origin and destination:
        query = True
        flights_data = Flight.objects.filter(
            origin__iexact=origin, 
            destination__iexact=destination
        ).order_by('price')
        
        if not flights_data.exists():
            flights_data = mock_flight_api(origin, destination, departure_date)
            flights_data.sort(key=lambda x: x.price)
            
    return render(request, 'flights.html', {
        'flights': flights_data,
        'query': query
    })

def book_flight(request):
    if request.method == 'POST':
        # Get data from form
        passenger_name = request.POST.get('passenger_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        passengers = request.POST.get('passengers', 1)
        
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        departure_date = request.POST.get('departure_date')
        return_date = request.POST.get('return_date', None)
        cabin_class = request.POST.get('cabin_class')
        
        seat_preference = request.POST.get('seat_preference', '')
        special_requests = request.POST.get('special_requests', '')
        
        # Save to DB
        booking = FlightBooking.objects.create(
            passenger_name=passenger_name,
            email=email,
            phone_number=phone_number,
            passengers=passengers,
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date if return_date else None,
            cabin_class=cabin_class,
            seat_preference=seat_preference,
            special_requests=special_requests
        )
        
        # ================================
        # 1️⃣ Email to ADMIN
        # ================================
        admin_subject = f"New Flight Booking from {passenger_name}"
        admin_message = f"""
Dear Admin,

A new flight booking has been made. Please review the details below:

Passenger Information:
--------------------------------------------------
Name:       {passenger_name}
Email:      {email}
Phone:      {phone_number}
Passengers: {passengers}

Travel Details:
--------------------------------------------------
Origin:      {origin}
Destination: {destination}
Departure:   {departure_date}
Return:      {return_date if return_date else 'N/A'}
Cabin Class: {cabin_class}
Seat Pref:   {seat_preference}
Requests:    {special_requests}

Best Regards,
Merka Automated System
"""
        try:
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                ['merkaflight@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            print("Admin email error:", e)

        # ================================
        # 2️⃣ Auto Reply to USER
        # ================================
        user_subject = "Flight Booking Confirmation - Merka SkyWays ✈️"
        user_message = f"""
Dear {passenger_name},

Thank you for booking with Merka SkyWays!

We have successfully received your flight booking request from {origin} to {destination}. 
Our team is currently processing your request and will contact you shortly with your finalized ticket and itinerary.

Booking Summary:
- Passengers: {passengers}
- Departure: {departure_date}
- Cabin: {cabin_class}

If you have any questions, feel free to reply to this email.

Safe travels!
The Merka SkyWays Team
"""
        try:
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print("User email error:", e)

        
        # We can re-render the flights page with a success flag
        # For simplicity, pass the required get parameters so the search is preserved if we want, or just return to index
        return render(request, 'flights.html', {
            'success': True,
            'booking': booking
        })
        
    return redirect('flights')
