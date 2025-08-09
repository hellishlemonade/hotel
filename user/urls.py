from django.urls import include, path

from .views import ProfileCreateView


urlpatterns = [
    path('registration/', ProfileCreateView.as_view()),
]
