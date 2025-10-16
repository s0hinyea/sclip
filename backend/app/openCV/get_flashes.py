import cv2
import numpy as np 

def get_flashes(frame, x, y, threshold=200):
    
    bgr = frame[y, x]                       # [B, G, R]
    avg = float(np.mean(bgr, dtype=np.float32))
    #using sum on NumPy array of unsigned 8-bit integer (0–255 only)
    #makes (200 + 200 + 200) / 3 wrap around 256 so they do 600 % 256 before dividing by 3
    #use np.mean instead and cast dtype to float32
    return avg, avg >= threshold
    

    """
    for flash in brightness:
        if int(flash) >= 230:
            count += 1
    
    return count 
    """