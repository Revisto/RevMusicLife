from django.urls import path
from . import views

urlpatterns = [
    path('currently-playing/', views.currently_playing_song, name='currently-playing-song'),
    path('test/', views.new_feature, name='new_feature'),
]