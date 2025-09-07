from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('bookings.urls')),
    path('api/profile/', include('profiles.urls')),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('api-auth/', include('rest_framework.urls')),
]
