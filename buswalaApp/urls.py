from .views import RegisterApi,login

from django.urls import path
from buswalaProject import settings

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('login/', login.as_view()),
    
]

