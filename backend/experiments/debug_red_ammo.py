import cv2
import numpy as np
from app.openCV.detect_ammo_change import get_ammo_roi_coords

video_path = "data/sample_clip_four.mp4"
clip = cv2.VideoCapture(video_path)

# Fast forward to 5.5 seconds (frame 330) where the text is red
clip.set(cv2.CAP_PROP_POS_FRAMES, 330)
ret, frame = clip.read()
clip.release()

if not ret:
    print("Failed to read frame 330")
    exit()

x1, x2, y1, y2 = get_ammo_roi_coords(frame)
roi = frame[y1:y2, x1:x2]

# 1. Original color
cv2.imwrite("experiments/debug_red_original.png", roi)

# 2. Grayscale conversion
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
cv2.imwrite("experiments/debug_red_grayscale.png", gray_roi)

# 3. Binary mask with 200 threshold
_, binary_roi_200 = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)
cv2.imwrite("experiments/debug_red_mask_200.png", binary_roi_200)

print(f"Average grayscale brightness of red text: {np.max(gray_roi)}")
print("Saved debug images to experiments/")
