from django.urls import path
from .views import ProfileDetail

urlpatterns = [
    path('me/', ProfileDetail.as_view(), name='profile_detail'),
]