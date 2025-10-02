import cv2
import numpy as np 
from pathlib import Path

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = normal_image[y, x] #Since going vertically in a python array is rows
                            #And going horizontally is columns
        print(f"Clicked at ({x}, {y})")
        print(f"Pixel BGR values: {pixel}")

def normalize_video_frame(frame, target_width=1920, target_height=1080):
    normalized_frame = cv2.resize(frame, (target_width, target_height))
    return normalized_frame

def get_roi(frame, x1, y1):
    
    roi = frame[y1,x1] # y = rows, x = cols
    averageBGR = sum(roi) / len(roi)
    isBright = averageBGR >= 200 
    
    return averageBGR, isBright
    

    """
    for flash in brightness:
        if int(flash) >= 230:
            count += 1
    
    return count 
    """

def load_and_extract(video_path, frames_RMS, bounds=0):

    clip = cv2.VideoCapture(video_path)
    if not clip.isOpened():
        print("Error: didnt open video")
    fps = clip.get(cv2.CAP_PROP_FPS) or 60.0
    
        
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    for k,v in frames_RMS.items(): #keys = timestamp , value = RMS
        timestamp = float(k) 
        frame_idx = (int(round(timestamp * fps))) - 10

        clip.set(cv2.CAP_PROP_POS_FRAMES, frame_idx) #makes the video to be set at a certain frame
        
        boo, frame = clip.read()
        
        if boo:
            
            image_path = BASE_DIR / "data" / f"{k}.png"
        
            normal_frame = cv2.resize(frame, (1920, 1080))
            #cv2.namedWindow('Image') #create a window
            
            
            #cv2.imshow('Image', normal_frame) #opens window with frame
            #cv2.waitKey(0)# 0 = press any key to close
            #cv2.destroyAllWindows()
            
            luminance, didFlash = get_roi(normal_frame, 1141, 652)
            print(f"Frame Num: {frame_idx} had brightness: {luminance}. Did it Flash? {didFlash} at Second {k}")

        else:
            return False 
 
    return True




"""
namedWindow: Creates an empty window (like an empty picture frame)
imshow: Puts an image into that window (like putting a picture in the frame)

"""




    

