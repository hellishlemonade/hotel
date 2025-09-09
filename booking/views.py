from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
)
from django.urls import reverse_lazy

from .forms import BookingCreateForm
from .models import Booking
from catalog.models import HotelRoom


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'booking/booking_create.html'
    success_url = reverse_lazy('profile')

    def get_room(self):
        return get_object_or_404(
            HotelRoom,
            slug=self.kwargs['slug']
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['room'] = self.get_room()
        kwargs['guest'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.get_room()
        return context

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.room = form.room
        booking.guest = form.guest
        booking.save()
        return super().form_valid(form)
