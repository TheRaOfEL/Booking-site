from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    REGIONS = [
        ("Africa", "Africa"),
        ("Asia", "Asia"),
        ("Europe", "Europe"),
        ("Middle East", "Middle East"),
        ("North America", "North America"),
        ("South America", "South America"),
        ("Oceania", "Oceania"),
    ]

    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=50, choices=REGIONS, default="Africa")

    def __str__(self):
        return f"{self.name} ({self.region}) - ${self.price}"


class TravelBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="travel_bookings")
    destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="bookings")
    travel_date = models.DateField()
    travel_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ("booked", "Booked"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ], default="")

    def __str__(self):
        return f"{self.user.username} -> {self.destination.name} on {self.travel_date} at {self.travel_time} ({self.status})"
