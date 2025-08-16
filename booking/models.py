from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model

from catalog.models import HotelRoom


User = get_user_model()


class Booking(models.Model):

    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Гость',
        related_name='bookings'
    )
    room = models.ForeignKey(
        HotelRoom,
        on_delete=models.CASCADE,
        verbose_name='Номер',
        related_name='bookings'
    )
    check_in_date = models.DateField('Дата заселения')
    check_out_date = models.DateField('Дата выезда')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    guest_count = models.PositiveSmallIntegerField(
        'Количество гостей',
        validators=[MinValueValidator(1, 'Минимум 1 гость')]
    )
    total_price = models.DecimalField(
        'Общая стоимость',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ('-created_at',)
        unique_together = ('room', 'check_in_date', 'check_out_date')

    def __str__(self):
        return f'Бронирование: {self.id} / {self.guest} / {self.room}'

    def clean(self):
        if self.guest_count > self.room.max_number_of_guests:
            raise ValidationError(
                'Значение не может быть больше чем в связанной модели')
        if self.check_in_date >= self.check_out_date:
            raise ValidationError(
                'Дата выезда должна быть позже даты заселения')
        if self.check_in_date < timezone.now().date():
            raise ValidationError('Дата заселения не может быть в прошлом')
        return super().clean()
