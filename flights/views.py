from django.shortcuts import render, get_object_or_404
from .models import Flight, Passenger
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, "index.html", {
        'flights': Flight.objects.all()
    })

def flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)  # Handle missing flights
    return render(request, "flight.html", {
        'flight': flight,
        'passengers': flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flight=flight).all()
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = get_object_or_404(Flight, pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flight.add(flight)
        return HttpResponseRedirect(reverse("flight", args=(flight_id,)))