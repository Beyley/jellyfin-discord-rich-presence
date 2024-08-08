import time
import logging
import requests
from pypresence import Presence, ActivityType
from dotenv import load_dotenv
import os

load_dotenv()

# Setup logging
logging.basicConfig(filename='jellyfin_rpc.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Starting Jellyfin Discord RPC script.")

# Jellyfin setup
jellyfin_url = os.getenv('JELLYFIN_URL')
api_key = os.getenv('JELLYFIN_API_KEY')
user_id = os.getenv('JELLYFIN_USER_ID')
headers = {
    'X-Emby-Token': api_key,
    'Content-Type': 'application/json'
}

# Discord setup
client_id = os.getenv('DISCORD_CLIENT_ID')
RPC = Presence(client_id)

def connect_rpc():
    try:
        RPC.connect()
        logging.info("Connected to Discord RPC.")
    except Exception as e:
        logging.error(f"Error connecting to Discord RPC: {e}")

connect_rpc()

def get_current_playing():
    url = f"{jellyfin_url}/Sessions?activeWithinSeconds=1"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sessions = response.json()
        return sessions
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching current playing item: {e}")
        return None

def get_album_cover_url(item_id, image_type="Primary", max_width=300):
    return f"{jellyfin_url}/Items/{item_id}/Images/{image_type}?maxWidth={max_width}&quality=90"

def extract_now_playing(sessions):
    if not sessions:
        return None
    for session in sessions:
        now_playing = session.get('NowPlayingItem')
        play_state = session.get('PlayState')
        if now_playing and play_state:
            artists = [artist.get('Name') for artist in now_playing.get('ArtistItems', [])]
            if not artists:
                artists = [artist.get('Name') for artist in now_playing.get('AlbumArtists', [])]

            album_cover_url = get_album_cover_url(now_playing.get('Id'))

            song_info = {
                'Name': now_playing.get('Name'),
                'Artists': artists,
                'Album': now_playing.get('Album'),
                'RunTimeTicks': now_playing.get('RunTimeTicks'),
                'PositionTicks': play_state.get('PositionTicks'),
                'AlbumCoverUrl': album_cover_url
            }
            logging.info(f"Now playing item: {song_info}")
            return song_info
    logging.debug("No currently playing item found.")
    return None

def format_time(ticks):
    seconds = ticks // 10**7
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"

def ensure_minimum_length(text, min_length=2):
    return text if len(text) >= min_length else text + ' ' * (min_length - len(text))

def update_discord_presence(song_info):
    try:
        current_time = format_time(song_info['PositionTicks'])
        total_time = format_time(song_info['RunTimeTicks'])

        start_time = int(time.time() - song_info['PositionTicks'] // 10**7)
        end_time = start_time + song_info['RunTimeTicks'] // 10**7

        logging.debug(f"Current time: {current_time}, Total time: {total_time}")

        album_name = ensure_minimum_length(song_info['Album'])

        RPC.update(
            activity_type=ActivityType.LISTENING,
            details=song_info['Name'],
            state=f"by {', '.join(song_info['Artists'])} from {song_info['Album']}",
            start=start_time,
            end=end_time,
            large_image=song_info['AlbumCoverUrl'],
            large_text=album_name,
            small_text=f"{current_time} / {total_time}"
        )
    except Exception as e:
        logging.error(f"Error updating Discord presence: {e}")
        if 'The pipe was closed' in str(e):
            logging.info("Attempting to reconnect to Discord RPC.")
            connect_rpc()

try:
    while True:
        sessions = get_current_playing()
        now_playing_item = extract_now_playing(sessions)
        if now_playing_item:
            update_discord_presence(now_playing_item)
        else:
            RPC.clear()
            logging.info("Cleared Discord presence.")
        time.sleep(5)  # Check every 5 seconds
except KeyboardInterrupt:
    logging.info("Script interrupted by user.")
    RPC.clear()
    logging.info("Closed Discord RPC connection.")
