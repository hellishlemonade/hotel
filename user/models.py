from django.contrib.auth.models import AbstractUser
from django.db import models

from hotel.constants import NAME_MAX_LENGTH


class Profile(AbstractUser):

    email = models.EmailField('Email', unique=True)
    USERNAME_FIELD = 'email'
    username = None
    first_name = models.CharField('Имя', max_length=NAME_MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=NAME_MAX_LENGTH)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    def __str__(self):
        return self.email
