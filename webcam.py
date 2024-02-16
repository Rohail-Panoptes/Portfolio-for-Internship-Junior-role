import cv2

# Initialize the camera
cam_port = 0
cam = cv2.VideoCapture(cam_port)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('hack.avi', fourcc, 20.0, (640, 480))

# Record video for 2 minutes
duration = 120  # in seconds
start_time = cv2.getTickCount() / cv2.getTickFrequency()

while True:
    # Read a frame from the camera
    ret, frame = cam.read()

    # If the frame is read correctly
    if ret:
        # Write the frame to the output video
        out.write(frame)

        # Display the frame
        cv2.imshow('Panoptes', frame)

        # Break the loop if 2 minutes have passed
        elapsed_time = (cv2.getTickCount() / cv2.getTickFrequency()) - start_time
        if elapsed_time >= duration:
            break

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error reading frame")
        break

# Release the camera and video writer
cam.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
