#!/usr/bin/env python3
"""
Simple voice-controlled light system for Bibl
Listens for speech containing "bibl" and "on"/"off"
"""

import speech_recognition as sr
import requests
import time

# Light control URLs
LIGHT_ON_URL = "http://192.168.0.29/on"
LIGHT_OFF_URL = "http://192.168.0.29/off"

def control_light(state):
    """Send HTTP request to control the light"""
    url = LIGHT_ON_URL if state == "on" else LIGHT_OFF_URL
    try:
        response = requests.get(url, timeout=2)
        print(f"✓ Light turned {state} (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")

def main():
    """Main loop - listens for speech and controls light"""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    print("=" * 50)
    print("Bibl Light Control")
    print("Say something with 'bibl' and 'on' or 'off'")
    print("Press Ctrl+C to exit")
    print("=" * 50)
    
    while True:
        try:
            # Listen for speech
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("\nListening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Recognize speech
            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"Recognized: {text}")
                
                # Check if "bibl" is in the speech
                if "jarvis" in text:
                    # Check for "on" or "off"
                    if "on" in text and "off" not in text:
                        print("→ Command: ON")
                        control_light("on")
                    elif "off" in text:
                        print("→ Command: OFF")
                        control_light("off")
                
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
            
            time.sleep(0.3)
            
        except sr.WaitTimeoutError:
            continue
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
