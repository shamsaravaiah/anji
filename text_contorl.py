#!/usr/bin/env python3
"""
Voice-controlled light system (Raspberry Pi version)

- Listens continuously on a USB microphone
- If it hears "jarvis" + "on" -> GET /on
- If it hears "jarvis" + "off" -> GET /off
"""

import time
import requests
import speech_recognition as sr
from typing import Set

# ========= CONFIG =========
LIGHT_ON_URL = "http://192.168.0.29/on"
LIGHT_OFF_URL = "http://192.168.0.29/off"

WAKE_WORD = "jarvis"

LISTEN_TIMEOUT_SEC = 5
PHRASE_TIME_LIMIT_SEC = 5
COOLDOWN_SEC = 1.5

# From your device list:
# 2: streamplify Mic.: USB Audio (hw:3,0)
MIC_DEVICE_INDEX = 2


def control_light(state: str) -> None:
    url = LIGHT_ON_URL if state == "on" else LIGHT_OFF_URL
    try:
        r = requests.get(url, timeout=3)
        print(f"[HTTP] Light -> {state} (status={r.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"[HTTP] ERROR calling {url}: {e}")


def normalize_words(text: str) -> Set[str]:
    cleaned = []
    for ch in text.lower():
        cleaned.append(ch if ch.isalnum() or ch.isspace() else " ")
    return set(" ".join(cleaned).split())


def main() -> None:
    recognizer = sr.Recognizer()

    # Lock to the known-good USB mic
    try:
        microphone = sr.Microphone(device_index=MIC_DEVICE_INDEX)
        print(f"[MIC] Using device_index={MIC_DEVICE_INDEX}")
    except Exception as e:
        print(f"[MIC] ERROR opening microphone (device_index={MIC_DEVICE_INDEX}): {e}")
        print("[MIC] Run the mic list again and update MIC_DEVICE_INDEX if needed.")
        return

    print("=" * 60)
    print("Voice Light Control (Pi)")
    print(f"Wake word: {WAKE_WORD}")
    print("Say: 'jarvis on' or 'jarvis off'")
    print("Ctrl+C to exit")
    print("=" * 60)

    # Calibrate once
    with microphone as source:
        print("[MIC] Calibrating for ambient noise (1s)...")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        print(f"[MIC] Energy threshold set to: {recognizer.energy_threshold}")

    last_action_ts = 0.0

    while True:
        try:
            with microphone as source:
                print("\n[MIC] Listening...")
                audio = recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT_SEC,
                    phrase_time_limit=PHRASE_TIME_LIMIT_SEC
                )

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"[ASR] {text}")

                words = normalize_words(text)

                if WAKE_WORD in words:
                    now = time.time()
                    if now - last_action_ts < COOLDOWN_SEC:
                        print("[SYS] Cooldown active; ignoring.")
                        continue

                    if "on" in words and "off" not in words:
                        print("[CMD] ON")
                        control_light("on")
                        last_action_ts = now
                    elif "off" in words:
                        print("[CMD] OFF")
                        control_light("off")
                        last_action_ts = now
                    else:
                        print("[CMD] Wake word heard, but no on/off command.")

            except sr.UnknownValueError:
                print("[ASR] Could not understand audio")
            except sr.RequestError as e:
                print(f"[ASR] Speech recognition request error: {e}")

            time.sleep(0.1)

        except sr.WaitTimeoutError:
            continue
        except KeyboardInterrupt:
            print("\n[SYS] Shutting down...")
            break
        except Exception as e:
            print(f"[SYS] ERROR: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()

