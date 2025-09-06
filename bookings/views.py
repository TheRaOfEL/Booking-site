from rest_framework import viewsets, permissions, filters
from .models import Country, TravelBooking
from .serializers import CountrySerializer, TravelBookingSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]  # allow all users to see countires


    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'price']
    search_fields = ['name']
    ordering_fields = ['price', 'name']



class TravelBookingViewSet(viewsets.ModelViewSet):
    queryset = TravelBooking.objects.all()
    serializer_class = TravelBookingSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'destination__region', 'destination__name']  # filter by status or country
    search_fields = ['destination__name']  # search by country name
    ordering_fields = ['travel_date', 'travel_time', 'destination__price']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return TravelBooking.objects.filter(user=user)
        return TravelBooking.objects.all()  # fallback for no auth

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            user, _ = User.objects.get_or_create(username="testuser") # create a dummy user
        serializer.save(user=user)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = "cancelled"
        booking.save()
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)