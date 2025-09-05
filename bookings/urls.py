from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, TravelBookingViewSet

router = DefaultRouter()
router.register("countries", CountryViewSet)
router.register("bookings", TravelBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
