from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.HotelRoomListView.as_view(), name='rooms'),
    path(
        'catalog/<slug:slug>/',
        views.HotelRoomDetailView.as_view(),
        name='room'
    )
]
