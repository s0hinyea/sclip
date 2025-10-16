import librosa 

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