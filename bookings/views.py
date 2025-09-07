from rest_framework import viewsets, permissions, filters
from .models import Country, TravelBooking
from .serializers import CountrySerializer, TravelBookingSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .permissions import IsOwner, IsAdminOrReadOnly


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrReadOnly] # only admins can edit countries

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'price']
    search_fields = ['name']
    ordering_fields = ['price', 'name']


class TravelBookingViewSet(viewsets.ModelViewSet):
    queryset = TravelBooking.objects.all()
    serializer_class = TravelBookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['status', 'destination__region', 'destination__name']  # filter by status or country
    search_fields = ['destination__name']  # search by country name
    ordering_fields = ['travel_date', 'travel_time', 'destination__price']

    def get_queryset(self):
        return TravelBooking.objects.filter(user=self.request.user)  # shows only bookings of logged in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # create booking for current user

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = "cancelled"
        booking.save()
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
