import os
import re
import time
import yt_dlp
import spotipy
from fuzzywuzzy import fuzz
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
)

def is_spotify_id(value):
    return bool(re.match(r'^[0-9a-zA-Z]{22}$', value))

def is_similar(a, b, threshold=90):
    return fuzz.ratio(a.lower(), b.lower()) > threshold

def search_track(query, source='youtube'):
    opts = {'format': 'bestaudio/best', 'quiet': True, 'no_warnings': True, 'extract_flat': True}
    prefix = 'ytsearch1' if source == 'youtube' else 'scsearch1'
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            res = ydl.extract_info(f"{prefix}:{query}", download=False)
            if res and res.get('entries'):
                return res['entries'][0]['title']
    except Exception as e:
        print(f"Error searching {source} for '{query}': {e}")
    return None

def get_artist_tracks(artist_input):
    if is_spotify_id(artist_input):
        artist_id = artist_input
    else:
        res = sp.search(q=f'artist:{artist_input}', type='artist', limit=1)
        if not res['artists']['items']:
            print("Artist not found.")
            return [], None
        artist_id = res['artists']['items'][0]['id']

    try:
        artist = sp.artist(artist_id)
        artist_name = artist['name']
        print(f"\nArtist: {artist_name}")
    except:
        print("Error retrieving artist info.")
        return [], None

    tracks = []
    albums = sp.artist_albums(artist_id, album_type='album,single', limit=50)

    while True:
        for album in albums['items']:
            for track in sp.album_tracks(album['id'])['items']:
                tracks.append({'name': track['name'], 'artist': artist_name, 'album': album['name']})
        if albums['next']:
            albums = sp.next(albums)
        else:
            break

    print(f"Found {len(tracks)} tracks.")
    return tracks, artist_name

def list_tracks(tracks):
    print("\nTracks:")
    for i, t in enumerate(tracks, 1):
        print(f"{i:02d}. {t['artist']} - {t['name']} (Album: {t['album']})")

def download_track(track, artist_name, source='youtube', output_dir='downloads'):
    artist_path = os.path.join(output_dir, artist_name)
    os.makedirs(artist_path, exist_ok=True)
    query = f"{track['artist']} - {track['name']}"
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{artist_path}/{track['artist']} - {track['name']} ({source}).%(ext)s",
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': False,
        'ignoreerrors': True,
    }
    prefix = 'ytsearch1' if source == 'youtube' else 'scsearch1'
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f"{prefix}:{query}"])
        print(f"Downloaded from {source}: {query}")
    except Exception as e:
        print(f"Error downloading {query} from {source}: {e}")

def download_with_comparison(tracks, artist_name):
    print("\nComparing SoundCloud and YouTube...")
    downloaded = set()
    for track in tracks:
        query = f"{track['artist']} - {track['name']}"
        if query in downloaded:
            print(f"Skipped duplicate: {query}")
            continue
        sc_title = search_track(query, 'soundcloud')
        if sc_title and is_similar(query, sc_title):
            print(f"SoundCloud match: {query}")
            download_track(track, artist_name, 'soundcloud')
            downloaded.add(query)
            continue
        yt_title = search_track(query, 'youtube')
        if yt_title and is_similar(query, yt_title):
            print(f"YouTube match: {query}")
            download_track(track, artist_name, 'youtube')
            downloaded.add(query)
        else:
            print(f"No match: {query}")

def main():
    print("=== Spotify Artist Downloader ===")
    artist_input = input("Enter artist name or Spotify ID: ").strip()
    tracks, artist_name = get_artist_tracks(artist_input)
    if not tracks:
        print("No tracks found.")
        return

    while True:
        print("\n1. Show track list")
        print("2. Download all (YouTube)")
        print("3. Smart download (SoundCloud + YouTube)")
        print("4. Exit")
        choice = input("Select: ").strip()

        if choice == '1':
            list_tracks(tracks)
        elif choice == '2':
            print("\nDownloading from YouTube...")
            for t in tracks:
                download_track(t, artist_name, 'youtube')
                time.sleep(0.5)
            print(f"\nDone. Check 'downloads/{artist_name}'")
        elif choice == '3':
            download_with_comparison(tracks, artist_name)
            print(f"\nDone. Check 'downloads/{artist_name}'")
        elif choice == '4':
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
