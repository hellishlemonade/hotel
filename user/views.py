from django.shortcuts import render
from django.views.generic import (
    CreateView,
)
from django.urls import reverse_lazy

from .forms import SignUpForm


class ProfileCreateView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('index')
