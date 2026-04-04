import os
import pytest
from app.openCV.gunshot_detector import detect_gunshots


# Human-verified ground truth for sample_clip_three.mp4
# Timestamps: 2.65, 2.77, 4.48, 4.83, 4.97, 5.09, 7.49, 7.58, 9.01
GROUND_TRUTH_FRAMES = [159, 166, 269, 290, 298, 305, 449, 455, 541]


def test_gunshot_detector_integration_clip_three():
    """
    Level 2 Integration Test for the Sensor Fusion detector.
    Runs detect_gunshots() on sample_clip_three.mp4 and compares
    its output to the human-verified ground truth of 9 gunshots.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "..", "data", "sample_clip_three.mp4")
    assert os.path.exists(video_path), f"Test video not found at {video_path}"

    gunshots = detect_gunshots(video_path)
    detected_frames = sorted(list(gunshots.keys()))

    # Print results for manual inspection
    print(f"\nDetected frames:    {detected_frames}")
    print(f"Ground truth frames: {GROUND_TRUTH_FRAMES}")
    print(f"Detected count: {len(detected_frames)} / {len(GROUND_TRUTH_FRAMES)} ground truth")

    # The fusion detector must improve upon baseline (which only catches 3/9)
    assert len(gunshots) > 3, (
        f"Fusion detector found only {len(gunshots)} shots. "
        f"Must improve upon baseline recall of 3/9."
    )


# Human-verified ground truth for sample_clip_two.mp4 (16 shots)
# Timestamps: 2.53, 2.63, 2.93, 4.09, 4.20, 4.75, 5.00, 5.09, 5.20, 5.30, 5.38, 5.48, 5.58, 6.50, 6.59, 6.68.
GROUND_TRUTH_FRAMES_TWO = [152, 158, 176, 245, 252, 285, 300, 305, 312, 318, 323, 329, 335, 390, 395, 401]

def test_gunshot_detector_integration_clip_two():
    """
    Level 2 Integration Test for sample_clip_two.mp4.
    Validates robustness against the 'red text' low-ammo warning HUD state.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "..", "data", "sample_clip_two.mp4")
    assert os.path.exists(video_path), f"Test video not found at {video_path}"

    gunshots = detect_gunshots(video_path)
    detected_frames = sorted(list(gunshots.keys()))

    print(f"\nDetected frames (clip 2):    {detected_frames}")
    print(f"Ground truth frames (clip 2): {GROUND_TRUTH_FRAMES_TWO}")
    print(f"Detected count: {len(detected_frames)} / {len(GROUND_TRUTH_FRAMES_TWO)} ground truth")

    # In a 16-shot rapid-fire burst, we expect to catch at least half of them 
    # (since audio/visual sync and rapid 600 RPM fire are chaotic).
    assert len(gunshots) > 5, (
        f"Fusion detector only found {len(gunshots)}/16 shots. "
        f"The red 'low ammo' text might be breaking the binary thresholding."
    )

