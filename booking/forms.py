from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, ButtonHolder, Submit, Field
from django import forms
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Booking, HotelRoom


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "check_in_date",
            "check_out_date",
            "guest_count",
        ]
        labels = {
            "check_in_date": "Дата заселения",
            "check_out_date": "Дата выезда",
            "guest_count": "Количество гостей",
        }
        widgets = {
            "check_in_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "check_out_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "guest_count": forms.NumberInput(
                attrs={"min": 1, "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        self.guest = kwargs.pop('guest', None)
        super().__init__(*args, **kwargs)
        today = timezone.now().date().isoformat()
        # Ограничиваем выбор дат сегодняшним днём и позже
        self.fields["check_in_date"].widget.attrs.setdefault("min", today)
        self.fields["check_out_date"].widget.attrs.setdefault("min", today)

        # Настройка crispy forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<div class="booking-form-title">Бронирование номера</div>'),
            Field('check_in_date', css_class='form-field'),
            Field('check_out_date', css_class='form-field'),
            Field('guest_count', css_class='form-field'),
            ButtonHolder(
                Submit('submit', 'Забронировать', css_class='btn-book-submit')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        if self.room and 'guest_count' in cleaned_data:
            if cleaned_data['guest_count'] > self.room.max_number_of_guests:
                self.add_error('guest_count',
                               'Максимальное количество гостей: '
                               f'{self.room.max_number_of_guests}'
                               )
        return cleaned_data
