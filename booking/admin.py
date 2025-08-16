from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Booking,
)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Админка для бронирований"""
    list_display = (
        'guest', 'room', 'guest_count', 'total_price'
    )
    list_filter = (
        'check_in_date', 'check_out_date', 'created_at',
        'guest_count'
    )
    search_fields = (
        'guest__email', 'guest__first_name', 'guest__last_name',
        'room__title'
    )
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'check_in_date'
    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('guest', 'room', 'guest_count')
        }),
        ('Даты', {
            'fields': (
                'check_in_date', 'check_out_date', 'created_at', 'updated_at')
        }),
        ('Финансовая информация', {
            'fields': ('total_price',)
        }),
    )
