from django.contrib import admin

from catalog.models import Hotel, HotelRoom


class HotelRoomInstanceInline(admin.StackedInline):
    model = HotelRoom


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'city')
    list_filter = ('country', 'city')


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_number_of_guests', 'price')
    list_filter = ('hotel', 'max_number_of_guests', 'price')
