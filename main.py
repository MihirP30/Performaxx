import requests
import pygame
import tempfile
import os

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
    """Download preview MP3 and play it."""
    if not preview_url:
        print("⚠️  No preview available for this song.")
        return

    # Download to a temp file
    r = requests.get(preview_url)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(r.content)
        tmp_path = tmp.name

    # Play with pygame
    pygame.mixer.init()
    pygame.mixer.music.load(tmp_path)
    pygame.mixer.music.play()
    print("🎶 Playing 30-second preview... (Ctrl+C to stop)")

    # Wait while playing
    try:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        pygame.mixer.music.stop()
        os.remove(tmp_path)

def main():
    print("🎧 Deezer Song Search & Preview Player 🎧")
    query = input("Enter a song or artist name: ").strip()
    if not query:
        print("Please enter a search term.")
        return

    tracks = search_deezer(query)
    if not tracks:
        print("No results found.")
        return

    show_results(tracks)

    track = tracks[0]
    print(f"▶ Now playing: {track['title']} — {track['artist']['name']}")
    play_preview(track["preview"])

if __name__ == "__main__":
    main()
