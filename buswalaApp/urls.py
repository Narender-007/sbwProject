from .views import RegisterApi,login,otp_verify,logout,driver_register,reviews,booking_create

from django.urls import path
from buswalaProject import settings

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('login/', login.as_view()),
    path("otp-verify/", otp_verify.as_view()),
    path("logout/", logout.as_view()),
    path("driver-register/",driver_register.as_view()),
    path('review/',reviews.as_view()),
    path('booking/',booking_create.as_view()),
    
]

