from django.urls import path

from .views import ProfileCreateView


urlpatterns = [
    path('registration/', ProfileCreateView.as_view(), name='signup'),
]
