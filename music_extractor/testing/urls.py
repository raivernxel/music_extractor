from django.urls import path
from . import views

urlpatterns = [
    # path("spotify-login/", views.spotify_login, name="spotify_login"),
    # path("callback/", views.spotify_callback, name="spotify_callback"),
    path("", views.add_to_playlist, name="add_to_playlist"),
]