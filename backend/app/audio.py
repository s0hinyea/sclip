from pathlib import Path
import librosa 
from moviepy.editor import VideoFileClip

def extract_audio(file_path, output_audio):
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

  