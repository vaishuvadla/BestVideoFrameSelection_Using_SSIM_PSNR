# FrameFit: Optimal Frame Selection with Quality Metrics

**FrameFit** is a Python-based application that extracts frames from video files, evaluates their quality using SSIM, PSNR, and MSE metrics, and selects the best frame by combining visual quality and human pose detection with MediaPipe Pose. The application also provides real-time progress tracking to enhance user interaction during processing.

## Features
- **Frame Extraction**: Extracts frames from video files using OpenCV.
- **Quality Evaluation**: Assesses frames based on SSIM, PSNR, and MSE metrics.
- **Pose Detection**: Uses MediaPipe Pose to ensure pose accuracy in frame selection.
- **Real-Time Progress**: Displays progress with Tkinter, providing smooth interaction during processing.
- **User-Friendly GUI**: Simple and intuitive interface for selecting videos and viewing the results.

## Technologies Used
- **Python**: Programming language.
- **OpenCV**: For video processing and frame extraction.
- **Tkinter**: For building the GUI and user interface.
- **MediaPipe**: For real-time human pose detection.
- **skimage**: For image quality metrics (SSIM, PSNR, MSE).

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/framefit.git
    cd framefit
    ```
2. Install dependencies:
    ```bash
    pip install opencv-python opencv-python-headless scikit-image mediapipe
    ```
3. Run the application:
    ```bash
    python main.py
    ```

## How It Works
- **Frame Extraction**: Frames are extracted from the selected video using OpenCV.
- **Quality Evaluation**: The quality of each frame is evaluated using SSIM, PSNR, and MSE, with the highest-quality frame selected.
- **Pose Detection**: MediaPipe Pose is used to detect human poses in the frames, ensuring the selected frame contains an accurate and clear pose.
- **Real-Time Progress**: A progress bar updates in real-time during frame extraction and evaluation.

## Usage
1. **Select Video**: Use the "Browse" button to select a video file.
2. **Start Processing**: Click "Start Processing" to begin the frame extraction and evaluation.
3. **View Best Frame**: After processing, the best frame will be displayed.

## Future Improvements
- Multi-threading for faster processing.
- Batch processing of multiple videos.
- Enhanced pose tracking and additional image quality metrics.
