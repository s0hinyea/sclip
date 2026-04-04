# SClip `noOCR` Branch — Architecture Guide

## The Problem
Our original gunshot detection algorithm relied solely on **muzzle flash brightness spikes**. This created a huge blindspot for rapid-fire weapons: because the weapon never fully returns to "dark" between bullets, the brightness delta is too small to trigger the threshold, causing us to miss 60-80% of bullets in a spray.

## The Solution: Sensor Fusion (Ammo + Audio)
Instead of relying on a flawed 3D visual effect, we now cross-validate the two most pristine signals in the game:
1. **The 2D UI (Ammo Counter)**
2. **The Audio Track (Gunshot Bangs)**

### Signal 1: Ammo Pixel Delta (SSIM)
*   **Where it lives:** `detect_ammo_change.py`
*   **How it works:** We crop the exact 1080p coordinates of the ammo box `(x: 1378-1452, y: 1005-1048)`. Instead of using OCR to *read* the number, we use Structural Similarity (SSIM) to instantly calculate if the shape of the text changed. 
*   **The Magic:** To prevent the translucent background or the red low-ammo text from ruining the math, we apply a **Binary Threshold of `>150`**. Everything brighter than 150 (white/red font) becomes stark white, and everything darker (translucent background/sky) becomes pitch black.

### Signal 2: Audio RMS (Librosa)
*   **Where it lives:** `find_peaks.py`
*   **How it works:** We scan the audio track for sudden massive spikes in RMS energy, identifying the exact timestamp of every loud sound.

### The "AND" Gate Orchestrator
*   **Where it lives:** `gunshot_detector.py`
*   **How it works:** When the ammo SSIM detects a visual change, we check if an audio peak exists within a `±8 frame` window (about ~133ms to account for standard AV sync delays in recordings). If both fire → **Confirmed Gunshot.** This beautifully rejects silent UI changes (reloads/weapon swaps) and loud non-ui changes (teammate gunfire/flashbangs).

## Testing Infrastructure
We now use `pytest` for absolute mathematical proof that our algorithms work.

### Running Tests
Inside your `backend` folder, run:
```bash
.venv/Scripts/python.exe -m pytest -v -s
```

### Integration Tests 
Inside `tests/test_gunshot_detector.py`, we have mapped human-verified arrays of exactly when bullets leave the gun for our sample clips (e.g. `[159, 166, 269...]`). The Pytest suite runs the video through our fusion detector and strictly asserts that our algorithm caught the exact shots a human did. 
_Note: We currently have ground truths set up for `sample_clip_three.mp4` and `sample_clip_two.mp4`._
