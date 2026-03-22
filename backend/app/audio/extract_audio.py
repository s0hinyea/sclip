import ffmpeg

async def extract_audio(file_path, output_audio):
  ##Extracts audio track from video file; saves as WAV(WaveForm Audio) file 

  try: 

    
    ffmpeg.input(file_path).output(output_audio).overwrite_output().run() 

    print(f"Extracted audio: {output_audio}")
    return True
  except Exception as e:
    print(f"Error: {e}")
    return False
