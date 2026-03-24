from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),   # added /
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("flights/", views.flights, name="flights"),
    path("book-flight/", views.book_flight, name="book_flight"),
]
