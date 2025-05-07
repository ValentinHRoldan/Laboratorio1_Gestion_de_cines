from django.urls import path
from rest_framework_simplejwt.views import (
TokenObtainPairView, TokenRefreshView,)
from .views import register

app_name = "usuario"

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/login/refresh/', TokenRefreshView.as_view()),
    path('api/register/', register)
 ]
