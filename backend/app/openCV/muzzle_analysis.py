import cv2
import numpy as np 
from pathlib import Path
from utils.ts_to_frame import ts_to_frame
from .get_flashes import get_flashes
from .normalize_frame import normalize_video_frame

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = normal_image[y, x] #Since going vertically in a python array is rows
                            #And going horizontally is columns
        print(f"Clicked at ({x}, {y})")
        print(f"Pixel BGR values: {pixel}")


def muzzle_analysis(video_path, frames_RMS, bounds=0):
    
    muzzle_flashes = {}
    clip = cv2.VideoCapture(video_path)
    if not clip.isOpened():
        print("Error: didnt open video")
    fps = clip.get(cv2.CAP_PROP_FPS) or 60.0
    
        
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    for k,v in frames_RMS.items(): #keys = timestamp , value = RMS
        frame_idx = k

        clip.set(cv2.CAP_PROP_POS_FRAMES, frame_idx) #makes the video to be set at a certain frame
        
        boo, frame = clip.read()
        
        if boo:
            
            image_path = BASE_DIR / "data" / f"{k}.png"
        
            normal_frame = cv2.resize(frame, (1920, 1080))
            #cv2.namedWindow('Image') #create a window
            
            
            #cv2.imshow('Image', normal_frame) #opens window with frame
            #cv2.waitKey(0)# 0 = press any key to close
            #cv2.destroyAllWindows()
            
            luminance, didFlash = get_flashes(normal_frame, 1141, 652)
            if luminance >= 200:
                muzzle_flashes[frame_idx] = luminance
                print(f"Frame Num: {frame_idx} had brightness: {luminance} at Second {k}")
        else:
            return False 
 
    return muzzle_flashes




"""
namedWindow: Creates an empty window (like an empty picture frame)
imshow: Puts an image into that window (like putting a picture in the frame)

"""




    

