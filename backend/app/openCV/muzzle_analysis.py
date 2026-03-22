import cv2
import numpy as np 
from .get_flashes import detect_flash

COOLDOWN_FRAMES = 2  # skip this many frames after a detection to avoid duplicates

def muzzle_analysis(video_path):
    """
    Scan every frame of the video for muzzle flashes independently.
    Uses brightness delta detection with flashbang rejection.
    Returns {frame_idx: luminance} for each detected flash.
    """
    
    muzzle_flashes = {}
    clip = cv2.VideoCapture(str(video_path))
    if not clip.isOpened():
        print("Error: didnt open video")
        return muzzle_flashes

    fps = clip.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Scanning {total_frames} frames for muzzle flashes (fps={fps})...")

    # Track previous frame brightness for delta comparison
    prev_roi_brightness = None
    prev_frame_brightness = None

    frame_idx = 0
    while frame_idx < total_frames:
        clip.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = clip.read()
        
        if not ret:
            break

        roi_brightness, frame_brightness, is_flash = detect_flash(
            frame, prev_roi_brightness, prev_frame_brightness
        )

        if is_flash:
            muzzle_flashes[frame_idx] = roi_brightness
            timestamp = round(frame_idx / fps, 3)
            print(f"Flash detected — frame {frame_idx} (t={timestamp}s), "
                  f"ROI brightness: {roi_brightness:.1f}, "
                  f"delta: {roi_brightness - (prev_roi_brightness or 0):.1f}")
            frame_idx += COOLDOWN_FRAMES  # skip ahead to avoid counting the same flash
            # Reset brightness tracking after cooldown skip
            prev_roi_brightness = None
            prev_frame_brightness = None
        else:
            frame_idx += 1
            prev_roi_brightness = roi_brightness
            prev_frame_brightness = frame_brightness

    clip.release()
    print(f"Visual scan complete: {len(muzzle_flashes)} flashes detected")
    return muzzle_flashes
