from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Country, TravelBooking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "region", "zip_code", "price"]


class TravelBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # shows user detail

    class Meta:
        model = TravelBooking
        fields = ["id", "user", "destination", "travel_date", "travel_time", "status"]
        read_only_fields = ["user"]

        def update(self, instance, validated_data):
            # Prevent changing destination
            validated_data.pop("destination", None)
            return super().update(instance, validated_data)