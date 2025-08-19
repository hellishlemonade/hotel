from slugify import slugify
from django.urls import reverse

from django.db import models
from django.core.validators import MaxValueValidator

from hotel.constants import (
    COUNTRY_MAX_LENGTH,
    CITY_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    TITLE_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    MAX_GUESTS_VALUE
)


class Hotel(models.Model):

    COUNTRY_CHOICES = (
        ('RU', 'Russia'),
        ('USA', 'United States of America')
    )

    title = models.CharField(
        'Название', unique=True, max_length=TITLE_MAX_LENGTH
    )
    country = models.CharField(
        'Страна', choices=COUNTRY_CHOICES, max_length=COUNTRY_MAX_LENGTH
    )
    city = models.CharField('Город', max_length=CITY_MAX_LENGTH)

    class Meta:
        verbose_name = 'отель'
        verbose_name_plural = 'Отели'
        ordering = ('country', 'title')

    def __str__(self):
        return f'Отель: {self.title}, Город: {self.city}'


def hotel_room_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.slug, filename)


class HotelRoom(models.Model):

    title = models.CharField(
        'Название', unique=True, max_length=TITLE_MAX_LENGTH
    )
    slug = models.SlugField(
        'Слаг', unique=True, max_length=SLUG_MAX_LENGTH, blank=True
    )
    hotel = models.ManyToManyField(Hotel, verbose_name='Отели')
    max_number_of_guests = models.PositiveSmallIntegerField(
        'Максимальное количество гостей',
        validators=[MaxValueValidator(
            MAX_GUESTS_VALUE,
            ('Превышено количество гостей, '
             f'введите значение меньше или равное {MAX_GUESTS_VALUE}')
        )]
    )
    description = models.TextField(
        'Описание', max_length=DESCRIPTION_MAX_LENGTH
    )
    price = models.PositiveIntegerField('Цена за ночь')
    main_img = models.ImageField(upload_to=hotel_room_directory_path)

    class Meta:
        verbose_name = 'номер'
        verbose_name_plural = 'Номера'
        ordering = ('title',)

    def __str__(self):
        return f'Номер: {self.title}, Отель: {self.hotel}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('room', kwargs={'slug': self.slug})
