FRAME_TOLERANCE = 3  # ±frames to consider a match between audio and visual

def verify_gunshots(audio, visual):
  """
  Cross-validate audio and visual detections using time-window matching.
  
  For each visual detection, check if any audio detection falls within 
  ±FRAME_TOLERANCE frames. This handles the ~1 frame offset between 
  when a flash is seen vs when the sound is registered.
  
  Returns list of verified frame indices (using visual frame as the anchor).
  """
  verified = []
  
  # Copy audio keys so we can remove matched ones to prevent double-counting
  unmatched_audio = set(audio.keys())

  for vis_frame in sorted(visual.keys()):
    for audio_frame in sorted(unmatched_audio):
      if abs(vis_frame - audio_frame) <= FRAME_TOLERANCE:
        verified.append(vis_frame)  # anchor to the visual frame
        unmatched_audio.discard(audio_frame)  # prevent double-matching
        break

  return verified