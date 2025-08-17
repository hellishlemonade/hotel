from django.urls import path

from .views import (
    ProfileCreateView,
    ProfileLoginView,
    ProfileLogoutView,
    PersonalAccountView,
)


urlpatterns = [
    path('registration/', ProfileCreateView.as_view(), name='signup'),
    path('login/', ProfileLoginView.as_view(), name='login'),
    path('logout/', ProfileLogoutView.as_view(), name='logout'),
    path('profile/', PersonalAccountView.as_view(), name='profile'),
]
