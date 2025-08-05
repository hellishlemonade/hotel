from django.contrib import admin

from catalog.models import Hotel, HotelRoom, Kind


class HotelRoomInstanceInline(admin.StackedInline):
    model = HotelRoom


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'city')
    list_filter = ('country', 'city')


@admin.register(Kind)
class KindAdmin(admin.ModelAdmin):
    list_display = ('title', 'number_of_guests')
    list_filter = ('number_of_guests',)
    inlines = [HotelRoomInstanceInline]


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind')
    list_filter = ('hotel', 'kind')
