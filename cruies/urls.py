from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),   # added /
    path("booking/", views.booking, name="booking"),   # added /
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
]
