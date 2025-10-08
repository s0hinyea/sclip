def verify_gunshots(audio, visual):
  verified = []

  for k in visual:
    if k in audio:
      verified.append(k)

  return verified