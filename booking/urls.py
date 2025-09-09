from django.urls import path

from . import views


urlpatterns = [
    path('create/<slug:slug>/', views.BookingCreateView.as_view(), name='create_booking'),
]
