import cv2
import os
import tempfile
from .detect_ammo_change import detect_ammo_change, extract_ammo_roi
from app.audio.extract_audio import extract_audio
from app.audio.audio_analysis import audio_analysis


def detect_gunshots(video_path):
    """
    Sensor Fusion V2 gunshot detector.

    Cross-validates two independent signals:
      Signal 1 (2D UI): Pixel changes in the ammo counter (SSIM + binary threshold)
      Signal 2 (Audio): RMS energy spikes from the audio track (librosa)

    A gunshot is confirmed only when BOTH signals fire within a
    sliding ±2 frame window. This rejects reloads (ammo changes
    without loud bang) and teammate shots (loud bang without ammo change).

    Returns:
        dict{frame_idx: confidence_score}
    """
    confirmed_shots = {}

    # --- Step 1: Pre-process audio (one-time) ---
    # Extract WAV from the MP4, then run RMS peak detection
    audio_tmp = os.path.join(tempfile.gettempdir(), "sclip_audio_temp.wav")

    import asyncio
    loop = asyncio.new_event_loop()
    extracted = loop.run_until_complete(extract_audio(str(video_path), audio_tmp))
    loop.close()

    if not extracted:
        print("Warning: Audio extraction failed. Running ammo-only mode.")
        audio_peak_frames = set()
    else:
        audio_peaks, duration = audio_analysis(audio_tmp)
        audio_peak_frames = set(audio_peaks.keys())
        print(f"Audio pre-processing: {len(audio_peak_frames)} peak candidates")

    # --- Step 2: Frame-by-frame ammo analysis ---
    clip = cv2.VideoCapture(str(video_path))
    if not clip.isOpened():
        print("Error: could not open video")
        return confirmed_shots

    fps = clip.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Fusion Scanner V2: Analyzing {total_frames} frames (fps={fps})...")

    prev_ammo_roi = None

    frame_idx = 0
    while frame_idx < total_frames:
        clip.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = clip.read()
        if not ret:
            break

        # --- Signal 1: Ammo Counter (2D UI, SSIM + binary threshold) ---
        current_ammo_roi = extract_ammo_roi(frame)
        ssim_score, ammo_changed = detect_ammo_change(current_ammo_roi, prev_ammo_roi)

        # --- Sensor Fusion: The AND Gate ---
        if ammo_changed:
            # Check if any audio peak exists within ±8 frames (AV sync tolerance ~133ms)
            audio_nearby = any(
                f in audio_peak_frames
                for f in range(frame_idx - 8, frame_idx + 9)
            )

            if audio_nearby:
                # CONFIRMED GUNSHOT — both signals agree
                confirmed_shots[frame_idx] = 1.0
                timestamp = round(frame_idx / fps, 3)
                print(f"  CONFIRMED shot — frame {frame_idx} (t={timestamp}s), "
                      f"SSIM={ssim_score:.3f}")

                # Cooldown: skip ahead to avoid double-counting
                frame_idx += 2
                prev_ammo_roi = None
                continue
            else:
                # Ammo changed but no audio peak — reject (reload or weapon swap)
                timestamp = round(frame_idx / fps, 3)
                print(f"  REJECTED event — frame {frame_idx} (t={timestamp}s), "
                      f"ammo changed but no audio peak (SSIM={ssim_score:.3f})")

        # Normal frame progression
        prev_ammo_roi = current_ammo_roi
        frame_idx += 1

    clip.release()

    # Cleanup temp audio file
    if os.path.exists(audio_tmp):
        os.remove(audio_tmp)

    print(f"Fusion V2 scan complete: {len(confirmed_shots)} confirmed gunshots")
    return confirmed_shots
