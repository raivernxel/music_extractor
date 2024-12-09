from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_song_view, name='music_extractor'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    # path('spotify-login/', views.spotify_login, name="spotify_login"),
]
