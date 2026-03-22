import cv2
import numpy as np 

# --- ROI Definition (resolution-relative) ---
# Muzzle region: lower-right area where the weapon sits in Valorant
# These are percentages of frame width/height
ROI_X_START = 0.50   # left edge of ROI (50% across)
ROI_X_END   = 0.65   # right edge of ROI (75% across)
ROI_Y_START = 0.55   # top edge of ROI (45% down)
ROI_Y_END   = 0.65  # bottom edge of ROI (75% down)

# --- Thresholds ---
DELTA_THRESHOLD = 15       # minimum brightness jump in the muzzle ROI to count as a flash
FLASH_DELTA_THRESHOLD = 45 # brightness jump in the muzzle ROI to count as a flashbang (we discard)
FLASH_RATIO_THRESHOLD = 1.8  # muzzle delta must be this many times larger than full-frame delta


def get_roi_brightness(frame, x_start, x_end, y_start, y_end):
    """
    Extract a rectangular ROI from the frame and return its mean brightness.
    Coordinates are in pixels.
    """
    roi = frame[y_start:y_end, x_start:x_end]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray_roi, dtype=np.float32))


def get_frame_brightness(frame):
    """Return the mean brightness of the entire frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return float(np.mean(gray, dtype=np.float32))


def get_roi_coords(frame):
    """
    Convert resolution-relative ROI percentages to pixel coordinates
    based on the actual frame dimensions.
    """
    h, w = frame.shape[:2]
    return (
        int(w * ROI_X_START),
        int(w * ROI_X_END),
        int(h * ROI_Y_START),
        int(h * ROI_Y_END),
    )


def detect_flash(frame, prev_roi_brightness, prev_frame_brightness):
    """
    Detect a muzzle flash using brightness delta analysis.
    
    Returns:
        (roi_brightness, frame_brightness, is_flash)
        
    Logic:
        1. Compute brightness delta in muzzle ROI vs previous frame
        2. Compute brightness delta of full frame vs previous frame
        3. If muzzle ROI spiked significantly AND the spike is localized
           (not a flashbang lighting up the whole screen), it's a flash.
    """
    x1, x2, y1, y2 = get_roi_coords(frame)
    
    roi_brightness = get_roi_brightness(frame, x1, x2, y1, y2)
    frame_brightness = get_frame_brightness(frame)
    
    # First frame — no previous data to compare against
    if prev_roi_brightness is None:
        return roi_brightness, frame_brightness, False
    
    # Delta = how much brighter is this frame vs the last one?
    roi_delta = roi_brightness - prev_roi_brightness
    frame_delta = frame_brightness - prev_frame_brightness
    
    # Condition 1: The muzzle ROI had a significant brightness spike
    roi_spiked = roi_delta >= DELTA_THRESHOLD and roi_delta <= FLASH_DELTA_THRESHOLD
    
    # Condition 2: The spike is localized to the muzzle area, not the whole screen
    # If the full frame also spiked by a similar amount, it's a flashbang or scene change
    if frame_delta > 0 and roi_spiked:
        flash_is_localized = (roi_delta / max(frame_delta, 1)) >= FLASH_RATIO_THRESHOLD
    else:
        flash_is_localized = roi_spiked  # full frame didn't spike, so any ROI spike is localized
    
    is_flash = roi_spiked and flash_is_localized
    
    return roi_brightness, frame_brightness, is_flash