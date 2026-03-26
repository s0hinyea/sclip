import pytest
import numpy as np
from app.openCV.get_flashes import detect_flash, get_roi_coords

# Test 1: First frame returns no flash
def test_detect_flash_first_frame(black_frame):
    # If prev_roi_brightness is None, is_flash should be False
    roi_b, frame_b, is_flash = detect_flash(black_frame, None, None)
    assert is_flash is False

# Test 2: No spike = no flash
def test_detect_flash_no_spike(black_frame):
    # Frame is black, prev was black. Delta is 0.
    roi_b, frame_b, is_flash = detect_flash(black_frame, 0.0, 0.0)
    assert roi_b == 0.0
    assert frame_b == 0.0
    assert is_flash is False

# Test 3: Muzzle spike = flash detected
def test_detect_flash_muzzle_spike(black_frame):
    # We modify the black frame to have a white square in the ROI
    frame = black_frame.copy()
    x1, x2, y1, y2 = get_roi_coords(frame)
    # Give it a +25 brightness spike in the ROI (valid delta range: 15-45)
    frame[y1:y2, x1:x2] = 25
    
    # Run detection pretending previous frame was pure black
    roi_b, frame_b, is_flash = detect_flash(frame, 0.0, 0.0)
    
    # It should detect a flash
    assert is_flash is True

# Test 4: Flashbang rejection
def test_detect_flash_flashbang_rejection(black_frame):
    # We modify the black frame to have a HUGE spike in the ROI
    frame = black_frame.copy()
    x1, x2, y1, y2 = get_roi_coords(frame)
    # Give it a +100 brightness spike (invalid delta range, >45 limit)
    frame[y1:y2, x1:x2] = 100
    
    roi_b, frame_b, is_flash = detect_flash(frame, 0.0, 0.0)
    
    # It should reject it
    assert is_flash is False

# Test 5: Global brightness spike rejection
def test_detect_flash_global_spike(mid_gray_frame):
    # Frame is mid-gray (128). Pretend previous frame was 100 everywhere.
    # The ROI delta is +28. The full frame delta is +28. The ratio is 1.0.
    # Flash ratio threshold is 1.8, so it should be rejected.
    roi_b, frame_b, is_flash = detect_flash(mid_gray_frame, 100.0, 100.0)
    
    # Both deltas are roughly equal, meaning it's a global brightness jump, not a localized flash
    assert is_flash is False
