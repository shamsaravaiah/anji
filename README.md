# Bibl Light Control

Voice-controlled light system that listens for "Hey Bibl, turn on/off light" commands and controls a light via HTTP requests.

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `pyaudio` on macOS, you may need to install portaudio first:
```bash
brew install portaudio
```

4. Run the script:
```bash
python voice_control.py
```

## Usage

- Say "Hey Bibl, turn on light" to turn the light on
- Say "Hey Bibl, turn off light" to turn the light off
- Press Ctrl+C to exit

## Configuration

You can modify the light control URLs in `voice_control.py`:
- `LIGHT_ON_URL`: URL to turn the light on
- `LIGHT_OFF_URL`: URL to turn the light off

## Troubleshooting

- Make sure your microphone is connected and working
- Ensure you have an internet connection (Google Speech Recognition requires internet)
- Check that the light control device is reachable at the configured IP address

# anji
