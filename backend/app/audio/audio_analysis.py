import librosa 
from utils.ts_to_frame import ts_to_frame
from .find_peaks import find_peaks

def audio_analysis(audio_path):
  
  time_series, sample_rate = librosa.load(audio_path)
  duration = len(time_series) / sample_rate
  audio_peaks = find_peaks(time_series, sample_rate)
  avg_rms = sum(audio_peaks[0]) / len(audio_peaks[0])
  max_peak = max(audio_peaks[0])
  threshold = round((avg_rms * 1.5), 3)
  frame_RMS = {}
  for index, peak in enumerate(audio_peaks[0]):
    if peak >= threshold:
      sample_num = index * 512
      timestamp = sample_num / sample_rate
      ts = ts_to_frame(timestamp)
      frame_RMS[ts] = peak

  return frame_RMS, duration, avg_rms, threshold
