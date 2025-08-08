from django.shortcuts import render
from django.views import generic

from .models import Hotel, HotelRoom, Kind


CATALOG_TEMPLATE_DIR = 'catalog/'


def index(request):
    num_hotels = Hotel.objects.all().count()
    num_rooms = HotelRoom.objects.all().count()
    num_kinds = Kind.objects.all().count()
    return render(
        request,
        f'{CATALOG_TEMPLATE_DIR}index.html',
        context={
            'num_hotels': num_hotels,
            'num_rooms': num_rooms,
            'num_kinds': num_kinds,
        }
    )


class HotelRoomListView(generic.ListView):
    model = HotelRoom
    context_object_name = 'rooms'
    paginate_by = 10


class HotelRoomDetailView(generic.DetailView):
    model = HotelRoom
    context_object_name = 'room'
