import requests
import time
import subprocess
import os
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_notification(summary, body, icon_path):
    subprocess.run([
        'gdbus', 'call', '--session',
        '--dest', 'org.freedesktop.Notifications',
        '--object-path', '/org/freedesktop/Notifications',
        '--method', 'org.freedesktop.Notifications.Notify',
        'Spotify', '42', icon_path,
        summary, body, '[]', '{}', '5000'
    ])

last_song = None

while True:
    r = requests.get("https://api.lanyard.rest/v1/users/1137093225576935485")
    data = r.json().get('data', {}).get('spotify', {})
    
    if 'timestamps' in data:
        song_title = data.get('song', 'Unknown Title')
        song_artist = data.get('artist', 'Unknown Artist')
        
        times = data['timestamps']
        end_time = times['end']
        ctime = int(time.time()) * 1000

        remaining_time_ms = end_time - ctime
        
        if remaining_time_ms <= 1500 and last_song is not None:
            last_song = None  # Reset last song when it ends
            time.sleep(1)
            continue
        
        if remaining_time_ms > 1500 and last_song != f"{song_title} - {song_artist}":
            notification_message = f"{song_title} By {song_artist}"
            icon_path = '/tmp/spotify-notify/spotify.png'
            send_notification('Now Playing', notification_message, icon_path)
            last_song = f"{song_title} - {song_artist}"

        remaining_time_seconds = remaining_time_ms / 1000
        minutes = int(remaining_time_seconds // 60)
        seconds = int(remaining_time_seconds % 60)
        total_time_seconds = (times['end'] - times['start']) / 1000
        progress_seconds = total_time_seconds - remaining_time_seconds
        progress_percentage = (progress_seconds / total_time_seconds) * 100

        clear_console()
        print(f"Now Playing: {song_title} - {song_artist}")
        print(f"Remaining time: {remaining_time_seconds:.2f} seconds")
        print(f"Remaining time: {minutes} minutes and {seconds} seconds")
        bar_length = 40
        filled_length = int(bar_length * progress_percentage // 100)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"[{bar}] {progress_percentage:.2f}%")

