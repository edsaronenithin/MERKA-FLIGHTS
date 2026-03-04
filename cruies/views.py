from django.shortcuts import render, redirect
from .forms import contactForm, bookingForm
from .models import Contact, Booking
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



def booking(request):
    if request.method == 'POST':
        form1 = bookingForm(request.POST)
        if form1.is_valid():
            email = form1.cleaned_data.get('email', '')
            fname = form1.cleaned_data.get('fname', '')
            lname = form1.cleaned_data.get('lname', '')
            cruise = form1.cleaned_data.get('cruise', 'N/A')
            mobile = form1.cleaned_data.get('mobile', 'N/A')
            nguest = form1.cleaned_data.get('nguest', 'N/A')
            cabin = form1.cleaned_data.get('cabin', 'N/A')
            message = form1.cleaned_data.get('message', 'None')

            form1.save()

            # Admin email
            send_mail(
                f"New Booking Request: {fname} {lname}",
                f"""
Dear Admin,

A new cruise booking request has been submitted. Please find the reservation details below:

Customer Information:
--------------------------------------------------
Name:    {fname} {lname}
Email:   {email}
Phone:   {mobile}

Reservation Details:
--------------------------------------------------
Cruise:  {cruise}
Guests:  {nguest}
Cabin:   {cabin}

Additional Message:
--------------------------------------------------
{message}

Kindly review this request and contact the customer accordingly.

Best Regards,
Merka Cruises Automated System
                """,
                settings.EMAIL_HOST_USER,
                ["merkaflight@gmail.com"]
            )

            # User confirmation email
            send_mail(
                "Your Merka Cruises Booking Request 🚢",
                f"""
Dear {fname} {lname},

Warm greetings from Merka Cruises!

Thank you for choosing us for your next adventure. Your booking request for the {cruise} cruise has been successfully received. 

Our reservation team is currently reviewing your details and will contact you shortly to confirm your booking and provide further information.

If you have any immediate questions, please feel free to reply directly to this email.

Warm Regards,
The Merka Cruises Reservation Team
                """,
                settings.EMAIL_HOST_USER,
                [email]
            )

            return render(request, 'index.html', {
                'form1': bookingForm(),
                'success': True,
                'name': fname
            })
    else:
        form1 = bookingForm()

    return render(request, 'index.html', {'form1': form1})

def user_login(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        if user is not None:
            auth_login(request, user)
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
