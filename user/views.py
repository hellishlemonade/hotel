from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DetailView,
)
from django.urls import reverse_lazy

from .forms import SignUpForm, LoginForm


User = get_user_model()


class ProfileCreateView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('index')


class ProfileLoginView(LoginView):
    form_class = LoginForm


class ProfileLogoutView(LogoutView):
    pass


class PersonalAccountView(LoginRequiredMixin, DetailView):
    context_object_name = 'user'
    login_url = '/auth/login/'

    def get_object(self):
        return User.objects.prefetch_related(
            'bookings',
            'bookings__room').get(id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookings'] = self.request.user.bookings.all()
        return context
