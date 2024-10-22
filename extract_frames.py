import cv2
import os

# Path to the directory where you want to save the frames
output_dir = 'D:/communication/project1/frames'

# Read the video file
cap = cv2.VideoCapture('D:/communication/project1/ctf.mp4')

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Initialize variables
frame_count = 0

# Read frames from the video
while True:
    ret, frame = cap.read()

    # Break the loop when the video ends
    if not ret:
        break

    # Save the frame as an image
    frame_name = f"frame_{frame_count}.jpg"
    frame_path = os.path.join(output_dir, frame_name)
    cv2.imwrite(frame_path, frame)

    # Increment the frame count
    frame_count += 1

# Release the video capture object and close the output directory
cap.release()
cv2.destroyAllWindows()
