import requests

def get_song_album_cover_url(artist: str, album: str) -> str | None:
    """
    Returns the album cover URL (usually a JPEG) using artist and album name,
    or None if not found.
    """
    query_url = "https://musicbrainz.org/ws/2/release/"
    params = {
        "query": f'release:{album} AND artist:{artist}',
        "fmt": "json"
    }
    headers = {
        "User-Agent": "AlbumCoverFetcher/1.0 (your_email@example.com)"
    }

    try:
        response = requests.get(query_url, params=params, headers=headers)
        response.raise_for_status()
        releases = response.json().get("releases", [])
        if not releases:
            return None
        mbid = releases[0]["id"]
        return f"https://coverartarchive.org/release/{mbid}/front-500"
    except Exception as e:
        print("Error:", e)
        return None

# Test example
#url = get_album_cover_url("Daft Punk", "Discovery")
#print("Cover URL:", url)
