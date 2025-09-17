from pathlib import Path

def build_paths(file):
  
  BASE_DIR = Path(__file__).resolve().parent.parent.parent
  video_path = BASE_DIR / "data" / file.filename
  audio_path = BASE_DIR / "data" / "sample.wav"
  return video_path, audio_path
   #the filepath: we will save it to the data folder with its original filename

async def save_file(file, video):
  
  content = await file.read() 
  #reads the file bytes from the upload object into memory
  #await lets us compelte other tasks while reading is done 
  with open(video, "wb") as f:
    f.write(content)


  """
      open(file_path, "wb") → “Create a new file at data/filename in write-binary mode.”
      If clip.mp4 already exists there, this will overwrite it.
      If it doesn’t exist, Python will make a new one.
      
    """

