from fastapi import FastAPI, File, UploadFile 
#import FastAPI: class for creating app instance that we will add routes to
import os 
import librosa
from moviepy import VideoFileClip
from audio import extract_audio, find_peaks
from pathlib import Path

app = FastAPI() 

@app.get("/health")
async def root():
  return {"message": "yo"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):


  """posting to this route means uploading a file. 
  UploadFile => FastAPI type for file uploads
  File(...) => input should come from a file in the request
  Together: Expect the user to attach one file, call it file!
  A video file is saved as a long sequence of bytes """
  
  
  BASE_DIR = Path(__file__).resolve().parent.parent
  video_path = BASE_DIR / "data" / file.filename
  print(video_path)
  audio_path = BASE_DIR / "data" / "sample.wav"
  #the filepath: we will save it to the data folder with its original filename
  
  content = await file.read() 
  #reads the file bytes from the upload object into memory
  #await lets us compelte other tasks while reading is done 
  with open(video_path, "wb") as f:
    f.write(content)


  """
      open(file_path, "wb") → “Create a new file at data/filename in write-binary mode.”
      If clip.mp4 already exists there, this will overwrite it.
      If it doesn’t exist, Python will make a new one.
      
    """
  extract_audio(video_path, audio_path)
  time_series, sample_rate = librosa.load(audio_path)
  duration = len(time_series) / sample_rate
  audio_peaks = find_peaks(time_series, sample_rate)
  avg_rms = sum(audio_peaks[0]) / len(audio_peaks[0])
  max_peak = max(audio_peaks[0])
  

  return {"video_name": file.filename, 
          "saved_to": video_path,
          "audio_array": audio_path,
          "time_series": time_series.shape,
          "sample_rate": sample_rate,
          "duration": duration,
          "first_sample": float(time_series[110250]),
          "last_sample": float(time_series[-1]), 
          "avg_peaks": avg_rms,
          "max_peak": max_peak}

