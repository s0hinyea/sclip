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
