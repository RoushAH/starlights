import _thread
import time
import uasyncio as asyncio
from machine import Pin

# Global variables to control server and message
server_running = False
message_to_blink = "HELLO WORLD"

# LED pin
led = Pin("LED", Pin.OUT)

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----'
}

async def server_task():
    global message_to_blink
    while server_running:
        print("Server is running...")
        # Simulate receiving a new message
        message_to_blink = "WORLD HELLO"
        await asyncio.sleep(10)  # Simulate server work by sleeping for 10 seconds

def start_event_loop():
    loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
    loop.create_task(server_task())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Event loop stopped.")

def control_server(start):
    global server_running
    server_running = start
    if start:
        _thread.start_new_thread(start_event_loop, ())
    else:
        loop = asyncio.get_event_loop()
        loop.stop()

def blink_morse_code(message):
    for char in message:
        if char in MORSE_CODE_DICT:
            code = MORSE_CODE_DICT[char]
            for symbol in code:
                if symbol == '.':
                    led.on()
                    time.sleep(0.2)
                    led.off()
                elif symbol == '-':
                    led.on()
                    time.sleep(0.6)
                    led.off()
                time.sleep(0.2)  # Gap between symbols
            time.sleep(0.6)  # Gap between letters
        elif char == ' ':
            time.sleep(1.4)  # Gap between words

def master_loop():
    global server_running, message_to_blink
    while True:
        current_hour, current_minute = time.localtime()[3], time.localtime()[4]
        if 6 <= current_hour < 20 and current_minute % 2 == 0:
            if not server_running:
                print("Starting server.")
                control_server(True)
        else:
            if server_running:
                print("Stopping server.")
                control_server(False)

        # Blink Morse code message
        if server_running:
            print(f"Blinking message: {message_to_blink}")
            blink_morse_code(message_to_blink)
        
        time.sleep(60)  # Sleep for a minute before rechecking

# Start the master loop in the main thread
if __name__ == "__main__":
    try:
        # Run the master loop
        master_loop()
    except KeyboardInterrupt:
        print("Program interrupted and stopped.")
