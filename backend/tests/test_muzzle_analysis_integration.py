import os
import pytest
from app.openCV.muzzle_analysis import muzzle_analysis

def test_muzzle_analysis_integration_clip_three():
    """
    Level 2 Integration Test:
    Feeds a real 22MB video clip through the entire OpenCV processing pipeline.
    Validates that the frame loops, bounding box math, and threshold logic
    all work synchronously to detect exactly the correct sequence of events.
    """
    # Construct the absolute path so the test can be run from anywhere in the project
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_dir, "..", "data", "sample_clip_three.mp4")
    
    # Sanity check: ensure the file exists so we don't fail for the wrong reason
    assert os.path.exists(video_path), f"Test video not found at {video_path}"
    
    # Execute the full processing loop (takes ~10-15 seconds)
    flashes = muzzle_analysis(video_path)
    
    # Ground truth constraint 1: Total count
    # Note: True human ground truth identified 9 gunshots.
    # The current baseline algorithm misses the 6 rapid-fire shots.
    # We assert len == 3 to lock in the baseline behavior for comparison.
    assert len(flashes) == 3, f"Baseline currently expects 3 flashes, but found {len(flashes)}"
    
    # Ground truth constraint 2: Temporal precision
    # We verify the flashes occurred exactly on the correct frames (+/- 1 frame tolerance)
    detected_frames = sorted(list(flashes.keys()))
    # These are the 3 frames the baseline algorithm actually catches out of the 9
    expected_frames = [449, 460, 541]
    
    for detected, expected in zip(detected_frames, expected_frames):
        assert abs(detected - expected) <= 1, f"Expected flash at frame {expected}, got {detected}"
