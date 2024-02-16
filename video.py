import cv2
import pyautogui
import time
import numpy as np

# Get screen size
screen_size = pyautogui.size()

# Define the codec using VideoWriter_fourcc() and create a VideoWriter object
# We set the frame rate to 10.0 fps here
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("screen_record.avi", fourcc, 10.0, screen_size)

# Get the start time
start_time = time.time()

while True:
    try:
        # Capture screen frame by frame
        img = pyautogui.screenshot()
        
        # Write the RGB image to file
        out.write(np.array(img))
        
        # Break the loop after 10 seconds
        if time.time() - start_time >= 60:
            break
    except Exception as e:
        break

# After the loop release the video capture and video write objects
out.release()
