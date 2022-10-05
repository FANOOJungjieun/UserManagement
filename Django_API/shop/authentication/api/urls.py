from django.urls import path, include # setting > urls.py에서 import include 추가
from .views import RegistrationAPIView


urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
]