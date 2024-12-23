import cv2
import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error
import mediapipe as mp
from PIL import Image, ImageTk  # Import PIL for image handling in tkinter

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to extract frames from a video and save them in a folder
def extract_frames(video_path, base_output_dir, skip_frames=1, progress_callback=None):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(base_output_dir, f"{video_name}_extractedimages")
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Error opening video file")
        return None

    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % skip_frames == 0:
            frame_name = f"frame_{frame_count}.jpg"
            frame_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(frame_path, frame)

        frame_count += 1
        if progress_callback:
            progress_callback(min(frame_count, total_frames), total_frames)

    cap.release()
    return output_dir

# Function to find the best frame with pose detection and quality metrics
def find_best_frame_with_pose(frames_dir, base_output_dir, progress_callback=None):
    best_frame_path = None
    best_combined_score = 0

    first_frame_path = os.path.join(frames_dir, 'frame_0.jpg')
    first_frame = cv2.imread(first_frame_path)
    if first_frame is None:
        return None

    frame_files = sorted(os.listdir(frames_dir))
    total_files = len(frame_files)

    for index, frame_file in enumerate(frame_files):
        current_frame_path = os.path.join(frames_dir, frame_file)
        current_frame = cv2.imread(current_frame_path)
        if current_frame is None:
            continue

        current_ssim = ssim(first_frame, current_frame, channel_axis=-1)
        mse = mean_squared_error(first_frame, current_frame)
        current_psnr = float('inf') if mse == 0 else psnr(first_frame, current_frame)

        combined_score = 0.5 * current_ssim + 0.3 * current_psnr

        if combined_score > best_combined_score:
            best_combined_score = combined_score
            best_frame_path = current_frame_path

        if progress_callback:
            progress_callback(index + 1, total_files)

    if best_frame_path:
        best_frame = cv2.imread(best_frame_path)
        output_dir = os.path.join(base_output_dir, "best_frame_with_pose")
        os.makedirs(output_dir, exist_ok=True)
        best_frame_output_path = os.path.join(output_dir, os.path.basename(best_frame_path))
        cv2.imwrite(best_frame_output_path, best_frame)

    return best_frame_path

# GUI Application
class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Selector")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f8ff")

        # Header
        header_label = tk.Label(root, text="Best Video Frame Selector", font=("Arial", 20, "bold"), bg="#4682b4", fg="white", pady=10)
        header_label.pack(fill=tk.X)

        # Video selection frame
        self.video_path = tk.StringVar()
        select_frame = tk.Frame(root, bg="#f0f8ff", pady=10)
        select_frame.pack(pady=20)
        tk.Label(select_frame, text="Select Video:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, padx=10)
        tk.Entry(select_frame, textvariable=self.video_path, width=40, font=("Arial", 12)).grid(row=0, column=1, padx=10)
        tk.Button(select_frame, text="Browse", command=self.browse_video, font=("Arial", 12), bg="#4682b4", fg="white").grid(row=0, column=2, padx=10)

        # Processing progress
        self.progress_label = tk.Label(root, text="Status: Waiting for user input", font=("Arial", 12), bg="#f0f8ff", anchor="w")
        self.progress_label.pack(fill=tk.X, padx=20)
        self.progress = ttk.Progressbar(root, length=500, mode='determinate')
        self.progress.pack(pady=10)

        # Action buttons
        action_frame = tk.Frame(root, bg="#f0f8ff")
        action_frame.pack(pady=10)
        self.start_button = tk.Button(action_frame, text="Start Processing", command=self.start_processing, font=("Arial", 14), bg="#32cd32", fg="white", padx=10)
        self.start_button.grid(row=0, column=0, padx=10)
        tk.Button(action_frame, text="Quit", command=self.root.quit, font=("Arial", 14), bg="#dc143c", fg="white", padx=10).grid(row=0, column=1, padx=10)

        # Output Frame for displaying the best frame
        self.output_frame = tk.Frame(root, bg="#f0f8ff", pady=10)
        self.output_frame.pack(pady=20)

    def browse_video(self):
        file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4 *.avi")])
        if file_path:
            self.video_path.set(file_path)

    def display_best_frame(self, best_frame_path):
        # Load the image and display it in the GUI
        img = Image.open(best_frame_path)
        img.thumbnail((400, 300))  # Resize image to fit the window
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        img_label = tk.Label(self.output_frame, image=img_tk)
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack()

    def start_processing(self):
        video_path = self.video_path.get()
        if not video_path:
            messagebox.showwarning("Warning", "Please select a video file!")
            return

        self.progress_label.config(text="Processing video...")
        self.progress['value'] = 0
        self.start_button.config(state=tk.DISABLED)  # Disable the button during processing

        def process_video():
            base_output_dir = "./output"
            os.makedirs(base_output_dir, exist_ok=True)

            def update_progress(current, total):
                self.progress['value'] = (current / total) * 100
                self.progress_label.config(text=f"Processing: {current}/{total} frames...")

            frames_dir = extract_frames(video_path, base_output_dir, skip_frames=10, progress_callback=update_progress)
            if frames_dir:
                self.progress_label.config(text="Finding best frame...")
                best_frame_path = find_best_frame_with_pose(frames_dir, base_output_dir, progress_callback=update_progress)

                if best_frame_path:
                    self.display_best_frame(best_frame_path)  # Display the best frame in GUI

            self.progress_label.config(text="Processing completed!")
            messagebox.showinfo("Success", "Video processing completed!")
            self.start_button.config(state=tk.NORMAL)  # Enable the button after processing

        threading.Thread(target=process_video).start()

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
