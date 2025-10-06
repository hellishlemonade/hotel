from django.urls import path

from . import views


urlpatterns = [
    path('', views.HotelRoomListView.as_view(), name='rooms'),
    path(
        'catalog/<slug:slug>/',
        views.HotelRoomDetailView.as_view(),
        name='room'
    ),
    path(
        'hotels/',
        views.HotelList.as_view(),
        name='hotel'
    )
]
