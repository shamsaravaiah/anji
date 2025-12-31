#!/usr/bin/env python3
"""
Simple text-based CLI light control for Bibl
Type "on" or "off" to control the light
"""

import requests

# Light control URLs
LIGHT_ON_URL = "http://192.168.0.29/off"
LIGHT_OFF_URL = "http://192.168.0.29/on"

def control_light(state):
    """Send HTTP request to control the light"""
    url = LIGHT_ON_URL if state == "on" else LIGHT_OFF_URL
    try:
        response = requests.get(url, timeout=2)
        print(f"✓ Light turned {state} (Status: {response.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main loop - asks for text input"""
    print("=" * 50)
    print("Bibl Light Control (Text Input)")
    print("Type 'on' to turn on, 'off' to turn off")
    print("Type 'quit' or 'exit' to stop")
    print("=" * 50)
    
    while True:
        try:
            # Ask for user input
            user_input = input("\nEnter command (on/off): ").strip().lower()
            
            # Handle quit commands
            if user_input in ['quit', 'exit', 'q']:
                print("\nShutting down...")
                break
            
            # Control light based on input
            if user_input == "on":
                control_light("on")
            elif user_input == "off":
                control_light("off")
            else:
                print(f"Unknown command: '{user_input}'. Please enter 'on' or 'off'")
        
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()