
userid = 1137093225576935485 # your discord user ID
# Dont touch bellow this line. (or it will break)
import requests, time, subprocess, os, sys
required_dir = "/tmp/spotify-notify"
files_required = ["spotify.png", "spotify-notify.py"]

if not os.path.exists(required_dir) or any(not os.path.isfile(os.path.join(required_dir, f)) for f in files_required):
    print("Required files missing. Please check the directory."); sys.exit(0)

if os.name != "posix": print("This script is built for Linux."); sys.exit(0)

def clear_console(): os.system('cls' if os.name == 'nt' else 'clear')
def send_notification(s, b, i): subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.freedesktop.Notifications',
                    '--object-path', '/org/freedesktop/Notifications', '--method',
                    'org.freedesktop.Notifications.Notify', 'Spotify', '42', i, s, b, '[]', '{}', '5000'])

last_song = None

while True:
    data = requests.get(f"https://api.lanyard.rest/v1/users/{userid}").json().get('data', {}).get('spotify', {})
    if 'timestamps' in data:
        title, artist = data.get('song', 'Unknown Title'), data.get('artist', 'Unknown Artist')
        times = data['timestamps']
        remaining_time_ms = times['end'] - int(time.time()) * 1000
        
        if remaining_time_ms <= 1500: last_song = None; time.sleep(1); continue
        
        if remaining_time_ms > 1500 and last_song != f"{title} - {artist}":
            send_notification('Now Playing', f"{title} By {artist}", os.path.join(required_dir, 'spotify.png'))
            last_song = f"{title} - {artist}"

        remaining_time_seconds = remaining_time_ms / 1000
        minutes, seconds = divmod(int(remaining_time_seconds), 60)
        total_time_seconds = (times['end'] - times['start']) / 1000
        progress_percentage = (total_time_seconds - remaining_time_seconds) / total_time_seconds * 100

        clear_console()
        print(f"Now Playing: {title} - {artist}\nRemaining time: {remaining_time_seconds:.2f} seconds\nRemaining time: {minutes} minutes and {seconds} seconds")
        bar_length = 40; filled_length = int(bar_length * progress_percentage // 100)
        print(f"[{'█' * filled_length}{'-' * (bar_length - filled_length)}] {progress_percentage:.2f}%")
