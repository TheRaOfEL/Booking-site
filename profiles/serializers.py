from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "first_name","last_name", "phone_number", "address", "nationality"]
        read_only_fields = ["user"]