from django.urls import path
from . import views

urlpatterns = [
    path('currently-playing/', views.currently_playing_song, name='currently-playing-song'),
    path('top-tracks/', views.top_tracks, name='top-tracks'),
]