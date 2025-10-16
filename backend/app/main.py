from fastapi import FastAPI, File, UploadFile 
from fastapi.middleware.cors import CORSMiddleware
#import FastAPI: class for creating app instance that we will add routes to
import os 
import librosa
from moviepy import VideoFileClip

from audio import extract_audio, find_peaks, audio_analysis
from openCV import get_flashes, normalize_video_frame, muzzle_analysis

from utils.file_utils import build_paths, save_file
from pathlib import Path

from validate import verify_gunshots


app = FastAPI() 

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://127.0.0.1:3000", "http://localhost:3000", "http://127.0.0.1:8000", "http://localhost:8000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/health")
async def root():
  return {"message": "yo"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):


  print(f"Received file: {file.filename}")
  print(f"Content type: {file.content_type}")
  

  """posting to this route means uploading a file. 
  UploadFile => FastAPI type for file uploads
  File(...) => input should come from a file in the request
  Together: Expect the user to attach one file, call it file!
  A video file is saved as a long sequence of bytes """
  
  video_path, audio_path = build_paths(file)
  await save_file(file, video_path)
  await extract_audio(str(video_path), str(audio_path))
  frames_RMS, duration, avgRms, tresh = audio_analysis(audio_path)
  
    
  bright_frames = muzzle_analysis(video_path, frames_RMS)
  gunshots = verify_gunshots(frames_RMS, bright_frames)

  

  return {
          "Heard" : frames_RMS,
          "Seen" : bright_frames,
           "Duration" : duration,
           "Verified" : gunshots
  }

