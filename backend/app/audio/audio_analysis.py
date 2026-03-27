import librosa 
from app.utils.ts_to_frame import ts_to_frame
from .find_peaks import find_peaks

def audio_analysis(audio_path):
  """
  Run onset-based audio analysis on a WAV file.
  Returns ({frame_idx: onset_strength}, duration)
  """
  
  time_series, sample_rate = librosa.load(audio_path)
  duration = len(time_series) / sample_rate
  
  # find_peaks now returns [(timestamp_seconds, strength), ...]
  onsets = find_peaks(time_series, sample_rate)
  
  # Convert timestamps to frame indices
  frame_onsets = {}
  for timestamp, strength in onsets:
    frame_idx = ts_to_frame(timestamp)
    frame_onsets[frame_idx] = round(strength, 4)

  print(f"Audio analysis: {len(frame_onsets)} onset candidates from {duration:.1f}s clip")
  return frame_onsets, duration
