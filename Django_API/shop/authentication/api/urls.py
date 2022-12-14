from django.urls import path, include # setting > urls.py에서 import include 추가
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView


urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('current', UserRetrieveUpdateAPIView.as_view()),
]