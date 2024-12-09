import os, clipboard
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from testing.views import write_excel
from pprint import pprint

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/spotify/callback/'
SCOPE = "playlist-modify-public playlist-modify-private"


def spotify_callback(request):
    print('1')
    sp_oauth = authenticate_spotify()
    print('2')
    code = request.GET.get("code")
    print('3')
    token_info = sp_oauth.get_access_token(code)
    print('4')
    request.session["token_info"] = token_info
    print('5')
    # return render(request, 'spotify/music_extractor.html', )
    return redirect('spotify:music_extractor')

# def spotify_callback(request):
#     """Handle the callback from Spotify after user authentication."""
#     sp = authenticate_spotify()
#
#     # Check if the user was redirected with an authorization code
#     token_info = sp.auth_manager.get_access_token(request.GET['code'])
#
#     # Save the token for future requests (this can be stored in session or DB)
#     sp = Spotify(auth=token_info['access_token'])
#
#     # Now that we have an authenticated client, we can interact with Spotify
#     message = "You are now connected to Spotify!"
#
#     # Perform any action you want, for example, display user info
#     user = sp.current_user()
#     message += f" Hello {user['display_name']}!"
#
#     # Return a message or redirect to another page
#     return render(request, 'spotify/music_extractor.html', {'message': message})

def authenticate_spotify():
    """Authenticate and return a Spotify client instance."""
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

def search_song(sp, track_name):
    """Search for a song on Spotify."""
    results = sp.search(q=track_name, limit=1, type='track')
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]  # Return the first search result
    return None

def spotify_login(request):
    sp_oauth = authenticate_spotify()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def add_song_to_playlist(sp, playlist_id, track_uri):
    """Add a song to a playlist by its URI."""
    sp.playlist_add_items(playlist_id, [track_uri])

def top_songs():
    song_counts = {}
    top_list = []
    with open("musics.txt", "r") as file:
        songs = file.read().split('\n')

    for song in songs:
        if song in song_counts:
            song_counts[song] += 1
        else:
            song_counts[song] = 1

    for song, count in song_counts.items():
        index = 0
        song_count = [song, count]

        for top_song in top_list:
            if top_song[1] > count:
                index += 1

        top_list.insert(index, song_count)

    return top_list

def add_songs(request):
    songs = request.POST.get('songs').strip().split('\n')
    playlist_id = request.POST.get('playlist_id')

    # sp = authenticate_spotify()
    token_info = request.session.get("token_info")
    sp = Spotify(auth=token_info["access_token"])

    # Replace with your Spotify Playlist ID
    # playlist_id = '31Pqb8sITkxzCVnxXwGkox'

    for song in songs:
        track_name = song.strip()
        song = search_song(sp, track_name)

        if song:
            music_found = f"{song['name']} by {', '.join(artist['name'] for artist in song['artists'])}"
            add_song_to_playlist(sp, playlist_id, song['uri'])

            with open("musics.txt", "r") as file:
                content = file.read()

            try:
                with open("musics.txt", "w") as file:
                    file.write(f'{content}{music_found}\n')
            except Exception as e:
                print(f'{music_found}\n')
                with open("musics.txt", "w") as file:
                    file.write(f'{content}')


def add_song_view(request):
    print('wew')
    text_area = ''
    playlist_id = ''
    top_list = []

    # write_excel(request)

    if request.method == "POST":
        # Get the name from the submitted form
        text_area = request.POST.get('comments')
        playlist_id = request.POST.get('playlist_id')
        songs = request.POST.get('songs')
        comments = text_area.split('\r\n\r\n')
        messages = "List all the song titles in this comments separate it with \\n.\n\n"

        for comment in comments:
            message_info = comment.split('\r\n')
            if len(message_info) > 1:
                messages += f'{message_info[1]}\n'

        clipboard.copy(messages)

        if songs != '':
            add_songs(request)

        tl = top_songs()
        top_list = {}

        for data_list in tl:
            top_list[data_list[0]] = data_list[1]

    return render(request, 'spotify/music_extractor.html', {'comments': text_area,
                                                            'playlist_id': playlist_id, 'top_list': top_list})
