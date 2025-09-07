from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Country, TravelBooking
from django.utils.html import strip_tags


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "region", "zip_code", "price"]

    # removes scripts/HTML and whitespace
    def validate_name(self, value):
        clean_value = strip_tags(value).strip()
        if not clean_value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Country name should only contain letters and spaces.")
        return clean_value

    def validate_region(self, value):
        return strip_tags(value).strip()

    def validate_zip_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Zip code must only contain digits.")
        return value


class TravelBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # shows user detail

    class Meta:
        model = TravelBooking
        fields = ["id", "user", "destination", "travel_date", "travel_time", "status"]
        read_only_fields = ["user"]

    # prevent booking of past dates
    def validate_travel_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Travel date cannot be in the past.")
        return value

    def validate(self, data):
        request = self.context.get("request")
        user = request.user if request else None

        if not user or not user.is_authenticated:
            return data

        travel_date = data.get("travel_date")
        travel_time = data.get("travel_time")
        destination = data.get("destination")

        # prevent duplicate bookings be the same user

    def validate(self, data):

        user = data.get("user")
        travel_date = data.get("travel_date")
        travel_time = data.get("travel_time")
        destination = data.get("destination")

        if TravelBooking.objects.filter(
                user=user,
                travel_date=travel_date,
                travel_time=travel_time,
                destination=destination
        ).exists():
            raise serializers.ValidationError("You already have a booking at this date and time.")
        return data

    # Prevent changing destination
    def update(self, instance, validated_data):
        if "destination" in validated_data:
            validated_data.pop("destination")
        return super().update(instance, validated_data)
