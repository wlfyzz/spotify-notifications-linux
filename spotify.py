
userid = 1137093225576935485
# Your discord user id: (you must be in discord.gg/lanyard for it to work)

print(r"""
           _  __                
          | |/ _|               
 __      _| | |_ _   _ ________
 \ \ /\ / / |  _| | | |_ /_ / 
  \ V  V /| | | | |_| |/ / / / 
   \_/\_/ |_|_|  \__, /___/___|
                   __/ |        
                   |___/         
https://x.com/wlfyzz || https://wlfyzz.com
""")

import requests, time, subprocess, os, sys


def check_and_install(required_dir, files_required):
    if not os.path.exists(required_dir) or any(not os.path.isfile(os.path.join(required_dir, f)) for f in files_required):
        try:
            subprocess.run(["git", "clone", "https://github.com/wlfyzz/spotify-notifications-linux", required_dir])
            return True
        except subprocess.CalledProcessError:
            return False
    return True

required_dir = os.path.expanduser("~/.local/share/spotify-notifier")
files_required = ["spotify.png", "spotify.py"]
if not check_and_install(required_dir, files_required):
    sys.exit(1)

def create_launcher(script_path):
    launcher_dir = os.path.expanduser("~/.local/bin")
    launcher_path = os.path.join(launcher_dir, "spotify-notify")
    os.makedirs(launcher_dir, exist_ok=True)
    launcher_content = f"#!/bin/bash\npython3 {script_path}\n"
    with open(launcher_path, "w") as f:
        f.write(launcher_content)
    subprocess.run(["chmod", "+x", launcher_path])

create_launcher(f"{required_dir}/spotify.py")

if os.name != "posix":
    print("This script is designed for Linux-like systems, Notifications will not work.")
    linux = False
else:
    linux = True

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def send_notification(s, b, i):
    if linux:
        subprocess.run(['gdbus', 'call', '--session', '--dest', 'org.freedesktop.Notifications', '--object-path', '/org/freedesktop/Notifications', '--method', 'org.freedesktop.Notifications.Notify', 'Spotify', '42', i, s, b, '[]', '{}', '5000'])

last_song = None
while True:
    try:
        data = requests.get(f"https://api.lanyard.rest/v1/users/{userid}").json().get("data", {}).get("spotify", {})
        data2 = requests.get(f"https://api.lanyard.rest/v1/users/{userid}").json().get("data", {}).get("discord_user", {})
    except:
        sys.exit(1)

    if not isinstance(data, dict):
        sys.exit(f"{data2['username']} is not listening to Spotify!")

    if "timestamps" in data:
        title, artist = data.get("song", "Unknown Title"), data.get("artist", "Unknown Artist")
        times = data["timestamps"]
        remaining_time_ms = times["end"] - int(time.time()) * 1000

        if remaining_time_ms <= 1500:
            last_song = None
            time.sleep(1)
            continue

        if remaining_time_ms > 1500 and last_song != f"{title} - {artist}":
            send_notification("Now Playing", f"{title} By {artist}", os.path.join(required_dir, "spotify.png"))
            last_song = f"{title} - {artist}"

        remaining_time_seconds = remaining_time_ms / 1000
        minutes, seconds = divmod(int(remaining_time_seconds), 60)
        total_time_seconds = (times["end"] - times["start"]) / 1000
        progress_percentage = (total_time_seconds - remaining_time_seconds) / total_time_seconds * 100

        clear_console()
        print(f"Now Playing: {title} - {artist}")
        print(f"Remaining time: {minutes} minutes and {seconds} seconds")

        bar_length = 40
        filled_length = int(bar_length * progress_percentage // 100)
        print(f"[{'█' * filled_length}{'-' * (bar_length - filled_length)}] {progress_percentage:.2f}%")
