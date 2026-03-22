"""
Debug tool: runs muzzle flash detection on a video and saves a screenshot
of every frame where a flash was detected. Each screenshot has the ROI
rectangle drawn on it so you can visually verify the detection region.

Usage:
    python -m openCV.debug_flashes <path_to_video>

Screenshots are saved to backend/data/debug_flashes/
"""

import cv2
import sys
import os
import numpy as np
from pathlib import Path

# Import detection logic
from .get_flashes import detect_flash, get_roi_coords, DELTA_THRESHOLD

COOLDOWN_FRAMES = 2  # match the value in muzzle_analysis.py


def debug_flashes(video_path):
    clip = cv2.VideoCapture(str(video_path))
    if not clip.isOpened():
        print(f"Error: couldn't open {video_path}")
        return

    fps = clip.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {video_path}")
    print(f"FPS: {fps}, Total frames: {total_frames}, Duration: {total_frames/fps:.1f}s")

    # Create output directory
    out_dir = Path(__file__).resolve().parent.parent.parent / "data" / "debug_flashes"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Clear old debug images
    for old_file in out_dir.glob("*.png"):
        old_file.unlink()
    print(f"Saving debug screenshots to: {out_dir}")

    prev_roi_brightness = None
    prev_frame_brightness = None
    flash_count = 0

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
            flash_count += 1
            timestamp = round(frame_idx / fps, 3)
            delta = roi_brightness - (prev_roi_brightness or 0)

            # Draw the ROI rectangle on the frame for visualization
            x1, x2, y1, y2 = get_roi_coords(frame)
            annotated = frame.copy()
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Add text labels
            label = f"Frame {frame_idx} | t={timestamp}s | ROI={roi_brightness:.1f} | delta={delta:.1f}"
            cv2.putText(annotated, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Save screenshot
            filename = out_dir / f"flash_{flash_count:03d}_frame{frame_idx}.png"
            cv2.imwrite(str(filename), annotated)
            print(f"  [{flash_count}] {label} -> saved {filename.name}")

            frame_idx += COOLDOWN_FRAMES
            prev_roi_brightness = None
            prev_frame_brightness = None
        else:
            frame_idx += 1
            prev_roi_brightness = roi_brightness
            prev_frame_brightness = frame_brightness

        if frame_idx % 500 == 0:
            print(f"  Scanned {frame_idx}/{total_frames} frames...")

    clip.release()
    print(f"\nDone! {flash_count} flashes detected. Screenshots saved to {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m openCV.debug_flashes <path_to_video>")
        sys.exit(1)
    
    debug_flashes(sys.argv[1])
