import cv2

def normalize_video_frame(frame, target_width=1920, target_height=1080):
    normalized_frame = cv2.resize(frame, (target_width, target_height))
    return normalized_frame