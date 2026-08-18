from django.shortcuts import render, redirect
from .forms import BookingForm


def home(request):
    return render(request, "bookings/home.html")


def book_session(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return render(request, "bookings/booking.html", {"form": BookingForm(), "booking": booking, "show_confirmation": True})
    else:
        form = BookingForm()
    return render(request, "bookings/booking.html", {"form": form})
