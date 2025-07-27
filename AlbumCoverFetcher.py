import requests

def get_song_album_cover_url(artist: str, album: str) -> str | None:
    """
    Returns the best available album cover image URL (front cover) for a given artist and album.
    Falls back from thumbnail to full image if needed.
    """
    headers = {
        "User-Agent": "AlbumCoverFetcher/1.0 (your_email@example.com)"
    }

    # Step 1: Search MusicBrainz
    mb_url = "https://musicbrainz.org/ws/2/release/"
    params = {
        "query": f'release:{album} AND artist:{artist}',
        "fmt": "json"
    }

    try:
        mb_resp = requests.get(mb_url, headers=headers, params=params)
        mb_resp.raise_for_status()
        releases = mb_resp.json().get("releases", [])
        if not releases:
            print("No releases found.")
            return None
        mbid = releases[0]["id"]
    except Exception as e:
        print("MusicBrainz error:", e)
        return None

    # Step 2: Check cover art availability
    caa_url = f"https://coverartarchive.org/release/{mbid}"
    try:
        caa_resp = requests.get(caa_url, headers=headers)
        caa_resp.raise_for_status()
        images = caa_resp.json().get("images", [])
        for img in images:
            if img.get("front"):
                return img.get("thumbnails", {}).get("large") or img.get("image")
        print("No front image found.")
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("No cover art found for this release.")
        else:
            print("CAA HTTP error:", e)
        return None
    except Exception as e:
        print("Error fetching cover art:", e)
        return None

# 🔍 Test
#url = get_album_cover_url("Boards of Canada", "Music Has the Right to Children")
#print("Cover URL:", url)
