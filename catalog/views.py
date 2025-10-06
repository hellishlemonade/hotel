from django.shortcuts import render
from django.views import generic

from .models import Hotel, HotelRoom


CATALOG_TEMPLATE_DIR = 'catalog/'


def index(request):
    num_hotels = Hotel.objects.all().count()
    num_rooms = HotelRoom.objects.all().count()
    return render(
        request,
        f'{CATALOG_TEMPLATE_DIR}index.html',
        context={
            'num_hotels': num_hotels,
            'num_rooms': num_rooms,
        }
    )


class HotelRoomListView(generic.ListView):
    model = HotelRoom
    context_object_name = 'rooms'
    paginate_by = 10


class HotelRoomDetailView(generic.DetailView):
    model = HotelRoom
    context_object_name = 'room'

    def get_queryset(self):
        return HotelRoom.objects.prefetch_related('hotel')


class HotelList(generic.ListView):
    model = Hotel
    context_object_name = 'hotels'
