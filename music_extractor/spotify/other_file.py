from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv, set_key
import os, requests, clipboard

load_dotenv()

# Define Spotify authentication URL
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_API_URL = 'https://api.spotify.com/v1/me'

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/spotify/callback/'

SCOPE = "playlist-modify-public playlist-modify-private"


def spotify_auth(request):
    # Define Spotify authentication parameters
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'user-library-read user-read-email',  # Add any required scopes
    }

    # Redirect user to Spotify's authentication page
    auth_url = f"{SPOTIFY_AUTH_URL}?client_id={params['client_id']}&response_type={params['response_type']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}"
    return redirect(auth_url)


def spotify_callback(request):
    # Spotify will redirect to this view with the authorization code
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Error: No authorization code found.", status=400)

    # Now you exchange the code for an access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data=token_data)
    token_info = response.json()

    # Save the token info (e.g., in the session or a database)
    access_token = token_info.get('access_token')
    refresh_token = token_info.get('refresh_token')

    set_key('.env', 'SPOTIFY_TOKEN', access_token)

    # You can use the access token to make requests to the Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    user_info = requests.get(SPOTIFY_API_URL, headers=headers).json()

    # You can now use user_info to get user data from Spotify
    return render(request, 'spotify/music_extractor.html', )

def authenticate_spotify():
    """Authenticate and return a Spotify client instance."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    ))

def search_song(sp, track_name):
    """Search for a song on Spotify."""
    results = sp.search(q=track_name, limit=1, type='track')
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]  # Return the first search result
    return None

def add_song_to_playlist(sp, playlist_id, track_uri):
    """Add a song to a playlist by its URI."""
    sp.playlist_add_items(playlist_id, [track_uri])

def add_songs(request):
    songs = request.POST.get('songs').split('\n')
    playlist_id = request.POST.get('playlist_id')

    sp = authenticate_spotify()

    # Replace with your Spotify Playlist ID
    # playlist_id = '31Pqb8sITkxzCVnxXwGkox'

    for song in songs:
        track_name = song.strip()
        song = search_song(sp, track_name)

        if song:
            music_found = f"{song['name']} by {', '.join(artist['name'] for artist in song['artists'])}"
            add_song_to_playlist(sp, playlist_id, song['uri'])

            with open("musics.txt", "w") as file:
                file.write(music_found)
        #
        # with open("musics.txt", "r") as file:
        #     content = file.read()
        #     print(content)

def form_view(request):
    text_area = ''
    playlist_id = ''
    if request.method == "POST":
        # Get the name from the submitted form
        text_area = request.POST.get('comments')
        playlist_id = request.POST.get('playlist_id')
        songs = request.POST.get('songs')
        comments = text_area.split('\r\n\r\n')
        messages = "List all the song titles in this comments separate it with \\n.\n\n"

        for comment in comments:
            message_info = comment.split('\r\n')
            print('len(message_info)', len(message_info))
            if len(message_info) > 1:
                messages += f'{message_info[1]}\n'

        clipboard.copy(messages)

        if songs != '':
            add_songs(request)

    return render(request, 'spotify/music_extractor.html', {'comments': text_area,
                                                            'playlist_id': playlist_id})


"""The Death
try "funky town" 😁
10-8
2417
Reply
View 62 replies

MZEDITZ（ャム姻)
pls do palm tree panic funk
10-8
364
Reply
View 7 replies

JAMES MIG BLOX FRUT PLAYER
Pls Filipino phonk is cool I promise
11-28
1
Reply

.
Try 21st century phonk
10-8
59
Reply
View 14 replies

jojo メ
Best new gen phonk song I've heard without too much bass and u rated it 5/10 lol
10-9
1270
Reply
View 22 replies

Juann
best phonk of the year dai
10-9
44
Reply
View 6 replies

PPNATAL X PPEMYU
plis do life force
10-8
7
Reply
View 1 reply

WATER..
Please try Chisme chisme Phonk
10-8
12
Reply
View 1 reply

Homixid3*!
Why nobody hating 😭
10-10
2439
Reply
View 19 replies

𝖘𝖐𝖝𝖇𝖎𝖉𝖎𝖋𝖙𝖇𝖑
one of the only funk songs which are acceptable to listen to
10-10
66
Reply
View 2 replies

Tommy
Why 5😭?
10-8
927
Reply
View 8 replies

🤓🎃
HELP I-😭 I DESIDED TO WEAR A PENCIL SKIRT IN SCHOOL AND THE BOYS YELLED "WOW HOURGLASS!" AND I INTRODUCED MYSELF.(I have a mommy voice) AND THEY ALL HAD NOSEBLEEDS😭😭
10-9
1
Reply
View 6 replies

majed ماجد
· Creator
WHAT SONG SHOULD I LISTEN TO NEXT?
10-8
54
Reply
View 105 replies

junewey6
Love the funky vibes and smooth moves in this video!
10-8
536
Reply

majed ماجد
· Creator
@BotRaper
10-8
316
Reply
View 28 more
Hide

Todd Slone
embrace it
10-19
0
Reply
View 1 reply

IslamIsTheTruth
Before I scroll, I just wan to thank Beyoncè
10-8
558
Reply
View 5 replies

☦️🇬🇪Slevakerr🇳🇱☦️
this can't be real 🙏😭
10-10
564
Reply
View 7 replies

🌵 Stick 🌵
i swear phonk reaction these days 💀😭
10-11
10
Reply

🤨𒉭
¿am I in YouTube shorts or what is this?
10-8
341
Reply
View 9 replies

Tnino_xt
Who’s here in 2025😭🔥💯🙏
10-18
42
Reply
View 6 replies

feller fan
Day 100 of asking for beeper 📟 funk
10-8
11
Reply
View 1 reply

.•🐈‍⬛🎸alex📓🗝️•.(Kira ver)
Try nirvana
10-9
8
Reply
View 2 replies

blackSnakeZz
I was boutta go crazy if u denied it
5d ago
0
Reply
View 1 reply

Mannyyyyyy
👧 : So what do u do for a living
10-11
134
Reply
View 2 replies

bond009
Who knows this song by the edits💀
10-15
1
Reply
View 1 reply

A.
My name is Aris 😭
10-8
5
Reply
View 6 replies

Michael
what about void super slowed?
10-8
3
Reply

Infantestrom
The song won't leave my brain 😂
10-8
231
Reply

CRZY • Zîñétsú⚡
bro try the Wada well phonk
10-8
3
Reply
View 3 replies

the honored zazu
did he get any 10/10 yet?
10-9
10
Reply
View 1 reply

Lamar edkw
it’s my birthday tdy
10-9
5
Reply
View 5 replies"""