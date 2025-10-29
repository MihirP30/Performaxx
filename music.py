import requests
import pygame
import tempfile
import os
import random

performative_male_songs = [
    "Clairo – Bags",
    "Laufey – From the Start",
    "The Marías – Hush",
    "Beabadoobee – Glue Song",
    "PinkPantheress – Just for me",
    "Men I Trust – Show Me How",
    "Boy Pablo – Everytime",
    "Mac DeMarco – My Kind of Woman",
    "Gus Dapperton – Prune, You Talk Funny",
    "Rex Orange County – Corduroy Dreams",
    "Steve Lacy – Dark Red",
    "Frank Ocean – Pink + White",
    "Dominic Fike – 3 Nights",
    "Omar Apollo – Evergreen (You Didn’t Deserve Me at All)",
    "Joji – Ew",
    "Still Woozy – Goodie Bag",
    "Vacations – Young",
    "Dayglow – Can I Call You Tonight?",
    "Bruno Major – Nothing",
    "Cavetown – Devil Town",
    "Harry Styles – Love of My Life",
    "Arctic Monkeys – I Wanna Be Yours",
    "Cigarettes After Sex – Apocalypse",
    "Phoebe Bridgers – Motion Sickness",
    "Mitski – First Love / Late Spring",
    "Lana Del Rey – Norman Fucking Rockwell",
    "Sufjan Stevens – Mystery of Love",
    "Bon Iver – Holocene",
    "The Japanese House – Saw You in a Dream",
    "Alex G – Runner"
]

def search_deezer(query):
    """Search Deezer for songs matching the query."""
    url = f"https://api.deezer.com/search?q={query}"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return data.get("data", [])

def show_results(tracks):
    """Display up to 5 tracks."""
    print("\nTop results:")
    for i, track in enumerate(tracks[:5], 1):
        print(f"{i}. {track['title']} — {track['artist']['name']}")

def play_preview(preview_url):
    if not preview_url:
        print("⚠️  No preview available for this song.")
        return

    r = requests.get(preview_url)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(r.content)
        tmp_path = tmp.name

    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()
    print("🎶 Playing 30-second preview...")

    # Do NOT block the main thread.
    # Optionally start a background cleanup thread:
    import threading, time
    def cleanup():
        time.sleep(35)
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    threading.Thread(target=cleanup, daemon=True).start()

def play_song():
    print("🎧 Deezer Song Search & Preview Player 🎧")
    query = performative_male_songs[random.randint(1, len(performative_male_songs)-1)]

    tracks = search_deezer(query)
    if not tracks:
        print("No results found.")
        return

    show_results(tracks)

    track = tracks[0]
    print(f"▶ Now playing: {track['title']} — {track['artist']['name']}")
    play_preview(track["preview"])

if __name__ == "__main__":
    play_song()
