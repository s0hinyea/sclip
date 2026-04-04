import pytest
import numpy as np
from app.openCV.detect_ammo_change import detect_ammo_change, get_ammo_roi_coords


# Test 1: First frame returns no change
def test_detect_ammo_change_first_frame():
    """When prev_roi is None (first frame), should return score=1.0, changed=False"""
    dummy_roi = np.zeros((50, 50), dtype=np.uint8)
    score, changed = detect_ammo_change(dummy_roi, None)
    assert score == 1.0
    assert changed is False


# Test 2: Identical frames = no change
def test_detect_ammo_change_identical():
    """Same image compared to itself should have SSIM ~1.0 and changed=False"""
    roi = np.full((50, 50), 100, dtype=np.uint8)
    score, changed = detect_ammo_change(roi, roi.copy())
    assert score >= 0.99
    assert changed is False


# Test 3: Significant text change = change detected
def test_detect_ammo_change_significant_change():
    """Simulating ammo text changing (e.g. '25' → '24') by painting different pixels"""
    roi_prev = np.full((50, 50), 100, dtype=np.uint8)
    roi_curr = roi_prev.copy()
    # Paint a white block simulating a digit change
    roi_curr[10:40, 10:20] = 255

    score, changed = detect_ammo_change(roi_curr, roi_prev)
    assert score < 0.85
    assert changed is True


# Test 4: Subtle background noise = no false change
def test_detect_ammo_change_subtle_noise():
    """A +5 brightness shift (background passing behind HUD) should not trigger"""
    roi_prev = np.full((50, 50), 100, dtype=np.uint8)
    roi_curr = np.clip(roi_prev.astype(np.int16) + 5, 0, 255).astype(np.uint8)

    score, changed = detect_ammo_change(roi_curr, roi_prev)
    assert score > 0.85
    assert changed is False


# Test 5: ROI coordinates scale correctly
def test_ammo_roi_coords_1080p():
    """At 1080p, the ammo ROI should land in the bottom-right corner"""
    fake_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    x1, x2, y1, y2 = get_ammo_roi_coords(fake_frame)

    # Verify the ROI is in the bottom-right quadrant
    assert x1 > 1920 * 0.5, "ROI x_start should be in the right half"
    assert y1 > 1080 * 0.5, "ROI y_start should be in the bottom half"
    assert x2 > x1, "ROI should have positive width"
    assert y2 > y1, "ROI should have positive height"
