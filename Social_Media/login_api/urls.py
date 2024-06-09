from django.urls import path
from .views import (
    LoginAPI,
    SignupAPI
)

urlpatterns = [
    path("login/", LoginAPI.as_view()),
    path("sign-up/", SignupAPI.as_view()),
]
