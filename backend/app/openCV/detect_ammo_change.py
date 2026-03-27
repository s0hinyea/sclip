import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# --- ROI Definition for Ammo Counter (hardcoded for 1080p) ---
# Measured directly from Valorant 1920x1080 gameplay.
# Top-left corner: (1378, 1005), Bottom-right corner: (1452, 1048)
AMMO_ROI_X1 = 1378
AMMO_ROI_X2 = 1452
AMMO_ROI_Y1 = 1005
AMMO_ROI_Y2 = 1048

# --- Thresholds ---
# SSIM ranges from -1 to 1 (1 = identical images).
# If SSIM drops below this, the ammo text visually changed.
SSIM_CHANGE_THRESHOLD = 0.85


def get_ammo_roi_coords(frame):
    """
    Return hardcoded pixel coordinates for the ammo counter ROI.
    V1: assumes 1920x1080 resolution only.
    """
    return (AMMO_ROI_X1, AMMO_ROI_X2, AMMO_ROI_Y1, AMMO_ROI_Y2)


def extract_ammo_roi(frame):
    """
    Extract the ammo counter region, convert it to grayscale,
    and apply binary thresholding to strip out the semi-transparent 
    background noise for a pristine SSIM comparison.
    """
    x1, x2, y1, y2 = get_ammo_roi_coords(frame)
    roi = frame[y1:y2, x1:x2]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Binary Thresholding: Any pixel brighter than 200 becomes solid white (255)
    # Everything else (the translucent background, map, sky) becomes solid black (0)
    _, binary_roi = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)
    
    return binary_roi


def detect_ammo_change(current_roi, prev_roi):
    """
    Compare current ammo ROI to previous frame's ammo ROI using SSIM.

    Returns:
        (ssim_score, changed: bool)
        
    If prev_roi is None (first frame), returns (1.0, False).
    """
    if prev_roi is None:
        return 1.0, False

    # Compute SSIM between the two grayscale ROI crops.
    # Use a smaller window size if the ROI is very small.
    win_size = min(7, current_roi.shape[0], current_roi.shape[1])
    if win_size % 2 == 0:
        win_size -= 1

    score, _ = ssim(prev_roi, current_roi, full=True, win_size=win_size, data_range=255)

    changed = bool(score < SSIM_CHANGE_THRESHOLD)

    return float(score), changed
