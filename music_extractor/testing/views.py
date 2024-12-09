from django.shortcuts import render
import pandas as pd


def write_excel(request):
    # Create a DataFrame
    # data = {'Name': ['Alice', 'Bob', 'Charlie'],
    #         'Age': [25, 30, 35]}
    #
    # df = pd.DataFrame(data)
    #
    # # Write the DataFrame to an Excel file
    # df.to_excel('file.xlsx', sheet_name='Sheet3', index=False)

    # new_data = {'Name': ['Dave', 'Eve'],
    #             'Age': [40, 45]}
    #
    # new_df = pd.DataFrame(new_data)
    #
    # # Append to the existing Excel file
    # # with pd.ExcelWriter('file.xlsx', mode='a', engine='openpyxl') as writer:
    # #     new_df.to_excel(writer, index=False, sheet_name='Sheet3', header=False)
    #
    # with pd.ExcelWriter('file.xlsx', mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
    #     new_df.to_excel(writer, index=False, sheet_name='Sheet3', startrow=writer.sheets['Sheet3'].max_row,
    #                     header=False)

    # Read the Excel file
    df = pd.read_excel('file.xlsx', sheet_name='Sheet3')

    # Display the data
    for key, value in df.items():
        for v in value:
            print(v)


# views.py
from django.shortcuts import redirect, render
from spotipy import Spotify

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings

# settings.py
SPOTIFY_CLIENT_ID = '88fd736385c344fa95fc400d842e48d3'
SPOTIFY_CLIENT_SECRET = '33609dbcaeb4486c8e28492c2f2e8bd8'
SPOTIFY_REDIRECT_URI = 'http://localhost:8000/spotify/callback/'


def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-modify-public playlist-modify-private"
    )

def spotify_login(request):
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = get_spotify_oauth()
    code = request.GET.get("code")
    token_info = sp_oauth.get_access_token(code)
    request.session["token_info"] = token_info
    return redirect("add_to_playlist")  # Redirect to your function to add songs

def add_to_playlist(request):
    if request.method == "POST":
        song_name = request.POST["song_name"]
        playlist_id = request.POST["playlist_id"]

        # Get token info from the session
        token_info = request.session.get("token_info")
        sp = Spotify(auth=token_info["access_token"])

        # Search for the song
        results = sp.search(q=song_name, type="track", limit=1)
        if results["tracks"]["items"]:
            track_id = results["tracks"]["items"][0]["id"]

            # Add the song to the playlist
            sp.playlist_add_items(playlist_id, [track_id])
            return render(request, "success.html", {"message": "Song added successfully!"})
        else:
            return render(request, "error.html", {"message": "Song not found."})

    return render(request, "testing/add_to_playlist.html")