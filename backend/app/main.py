from fastapi import FastAPI, File, UploadFile 
#import FastAPI: class for creating app instance that we will add routes to
import os 

app = FastAPI() 

@app.get("/health")
async def root():
  return {"message": "yo"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

  cwd = os.getcwd()
  see_data = os.path.isdir("data")

  """posting to this route means uploading a file. 
  UploadFile => FastAPI type for file uploads
  File(...) => input should come from a file in the request
  Together: Expect the user to attach one file, call it file!
  A video file is saved as a long sequence of bytes 

  file_path = f"data/{file.filename}"
  print(file_path)
  #the filepath: we will save it to the data folder with its original filename
  content = await file.read() 
  #reads the file bytes from the upload object into memory
  #await lets us compelte other tasks while reading is done 

  with open(file_path, "wb") as f:
    f.write(content)
     
     '
      open(file_path, "wb") → “Create a new file at data/filename in write-binary mode.”
      If clip.mp4 already exists there, this will overwrite it.
      If it doesn’t exist, Python will make a new one.
      
      '
  
  return {"filename": file.filename, "saved_to": file_path}"""

