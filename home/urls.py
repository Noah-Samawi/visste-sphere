"""Home URLS"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('google621ef7f3bda07ae5.html', views.google_verification, name='google_verification'),
]
