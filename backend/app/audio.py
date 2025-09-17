from pathlib import Path
import librosa 
from moviepy import VideoFileClip

async def extract_audio(file_path, output_audio):
  ##Extracts audio track from video file; saves as WAV(WaveForm Audio) file 

  try: 

    video_clip = VideoFileClip(file_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_audio, codec='pcm_s16le')
    audio_clip.close()
    video_clip.close()
    print(f"Extracted audio: {output_audio}")
    return True
  except Exception as e:
    print(f"Error: {e}")
    return False


def find_peaks(audio_data, sample_rate):

    try:
      print("Using RMS...")
      output_data = librosa.feature.rms(y=audio_data, frame_length=2048, hop_length=512)
      print("RMS Success")
      #Each chunk is 2048, and steps 512 after the end of a chunk for new chunk 
      #gives us 2d array where each number represeents the RMS energy for that time segment
      
      print(f"RMS SHAPE: {output_data.shape}")
      return output_data.tolist()
    except Exception as e:
      print(f"Error: {e}")
      return 

def audio_analysis(audio_path):
  
  time_series, sample_rate = librosa.load(audio_path)
  duration = len(time_series) / sample_rate
  audio_peaks = find_peaks(time_series, sample_rate)
  avg_rms = sum(audio_peaks[0]) / len(audio_peaks[0])
  max_peak = max(audio_peaks[0])
  threshold = round((avg_rms * 1.5), 3)
  rms_gunshots = {}
  for index, peak in enumerate(audio_peaks[0]):
    if peak >= threshold:
      rms_gunshots[index] = peak

  timestamp_gunshots = {}

  for index in rms_gunshots.keys():
    sample_num = index * 512
    timestamp = sample_num / sample_rate
    timestamp_gunshots[timestamp] = index

  return timestamp_gunshots, duration
