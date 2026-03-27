import cv2
from app.openCV.detect_ammo_change import get_ammo_roi_coords

video_path = "data/sample_clip_three.mp4"
clip = cv2.VideoCapture(video_path)
clip.set(cv2.CAP_PROP_POS_FRAMES, 500)
ret, frame = clip.read()
clip.release()

if not ret:
    print("Failed to read frame 100")
    exit()

x1, x2, y1, y2 = get_ammo_roi_coords(frame)
print(f"Frame size: {frame.shape[1]}x{frame.shape[0]}")
print(f"Ammo ROI coords: x=[{x1}, {x2}], y=[{y1}, {y2}]")

# Draw a green rectangle around the ammo ROI
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

output_path = "data/debug_ammo_roi.png"
cv2.imwrite(output_path, frame)
print(f"Saved to {output_path}")
