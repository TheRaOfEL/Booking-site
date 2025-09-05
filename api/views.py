from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    data = {
        "countries": request.build_absolute_uri(reverse("country-list")),
        "bookings": request.build_absolute_uri(reverse("travelbooking-list")),
    }
    return Response(data)