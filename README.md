Sure! Here’s a simple Markdown README for your project:

```markdown
# Spotify Notifier

A simple notification tool for Linux that displays the currently playing song on Spotify and provides console updates.

## Features

- Fetches currently playing song details from Spotify.
- Sends desktop notifications with song title and artist.
- Displays remaining playback time in the console.

## Requirements

- Python 3
- Git
- a discord account in discord.gg/lanyard

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wlfyzz/spotify-notifications-linux ~/
   ```

2. Run the script to set up:
   ```bash
   python3 setup.py
   ```

3. Ensure the script is executable:
   ```bash
   chmod +x ~/.local/bin/spotify-notify
   ```

4. Add the script to your PATH (if not already):
   ```bash
   export PATH="$PATH:$HOME/.local/bin"
   ```

## Usage

Run the notifier script:
```bash
~/.local/bin/spotify-notify
```

## Notes

- This script is designed for Linux environments.
- Ensure you have the required permissions to send notifications.

## License

This project is open-source and available under the MIT License.
```
