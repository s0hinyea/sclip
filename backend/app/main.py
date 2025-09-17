from fastapi import FastAPI, File, UploadFile 
#import FastAPI: class for creating app instance that we will add routes to
import os 
import librosa
from moviepy import VideoFileClip
from audio import extract_audio, find_peaks, audio_analysis
from utils.file_utils import build_paths, save_file
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
  
  video_path, audio_path = build_paths(file)
  await save_file(file, video_path)
  await extract_audio(str(video_path), str(audio_path))
  gunshots, duration = audio_analysis(audio_path)
    

  

  

  return {
          "Gunshots At" : gunshots,
          "Duration" : duration
  }
