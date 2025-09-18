import cv2
import numpy as np 
from pathlib import Path

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image[y, x] #Since going vertically in a python array is rows
                            #And going horizontally is columns
        print(f"Clicked at ({x}, {y})")
        print(f"Pixel BGF values: {pixel}")

def normalize_video_frame(frame, target_width=1920, target_height=1080):
    normalized_frame = cv2.resize(frame, (target_width, target_height))
    return normalized_frame
0
BASE_DIR = Path(__file__).resolve().parent.parent
image_path = BASE_DIR / 'data' / 'image1.png'


image = cv2.imread(image_path)
normal_image = cv2.resize(image, (1920, 1080))
cv2.namedWindow('Image') #create a window
cv2.setMouseCallback('Image', mouse_callback) #connect callback to window

"""
namedWindow: Creates an empty window (like an empty picture frame)
imshow: Puts an image into that window (like putting a picture in the frame)

"""

cv2.imshow('Image', normal_image)
cv2.waitKey(0)# 0 = press any key to close
cv2.destroyAllWindows()


    

