import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr

# Path to the directory containing the frames
frames_dir = 'D:/communication/project1/frames'

# Read the first frame
first_frame_path = f'{frames_dir}/frame_0.jpg'
first_frame = cv2.imread(first_frame_path)

# Initialize variables to store the best SSIM and PSNR values
best_ssim = 0
best_psnr = 0
best_frame_path = None

# Compare the first frame with the rest of the frames
for i in range(1, 10):  # Assuming there are 10 frames
    # Read the current frame
    current_frame_path = f'{frames_dir}/frame_{i}.jpg'
    current_frame = cv2.imread(current_frame_path)

    # Calculate SSIM and PSNR
    current_ssim = ssim(first_frame, current_frame, multichannel=True, win_size=3)
    current_psnr = psnr(first_frame, current_frame)

    # Update the best values if the current frame is better
    if current_ssim > best_ssim:
        best_ssim = current_ssim
        best_frame_path = current_frame_path

    if current_psnr > best_psnr:
        best_psnr = current_psnr
        best_frame_path = current_frame_path

# Save the best frame
best_frame = cv2.imread(best_frame_path)
cv2.imwrite('D:/communication/project1/best_frame/path_to_best_frame.jpg', best_frame)
