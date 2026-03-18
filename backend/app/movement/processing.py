import cv2
import numpy as np

# WHY: We downscale to this height because Optical Flow is EXPENSIVE. 
# Running it on 1080p takes ~100ms per frame. On 360p, it's ~10ms.
# Since we just need "is it moving?", 360p is plenty of resolution.
TARGET_HEIGHT = 360

def downscale_and_mask(frame):
    """
    Step 1: Simplify the image to what matters.
    
    Logic:
    1. Resize to make math faster.
    2. Black out pixels that move even when the player is still (Gun, HUD, Minimap).
    """
    h, w = frame.shape[:2]
    scale = TARGET_HEIGHT / h
    new_w = int(w * scale)
    
    # Resize - simple bilinear interpolation is fast and good enough
    resized = cv2.resize(frame, (new_w, TARGET_HEIGHT))
    
    # Create a mask where 255 = Keep, 0 = Ignore
    # We start with all white (keep everything)
    mask = np.ones((TARGET_HEIGHT, new_w), dtype=np.uint8) * 255
    
    # --- CENTER RECTANGLE MASK STRATEGY ---
    # Instead of masking corners, we ONLY keep the center rectangle.
    # This is simpler, faster, and focuses on the most reliable pixels.
    
    # Start with ALL BLACK (ignore everything)
    mask = np.zeros((TARGET_HEIGHT, new_w), dtype=np.uint8)
    
    # Define the center rectangle dimensions
    # We'll keep the center 50% width × 60% height
    rect_width_percent = 0.40
    rect_height_percent = 0.40
    
    rect_w = int(new_w * rect_width_percent)
    rect_h = int(TARGET_HEIGHT * rect_height_percent)
    
    # Calculate the top-left corner to center the rectangle
    start_x = (new_w - rect_w) // 2 - 30 
    start_y = (TARGET_HEIGHT - rect_h) // 2 - 30
    
    # Set the center rectangle to WHITE (keep these pixels)
    mask[start_y:start_y + rect_h, start_x:start_x + rect_w] = 255
    
    # Debug: Print the rectangle bounds
    # print(f"Center rectangle: ({start_x}, {start_y}) to ({start_x + rect_w}, {start_y + rect_h})")


    # Apply the mask to the frame purely for visualization/debug.
    # The actual algorithm will just use the 'mask' array to ignore pixels later.
    masked_frame = cv2.bitwise_and(resized, resized, mask=mask)
    
    return resized, mask, masked_frame

def stabilize_frame(prev_gray, curr_gray):
    """
    Step 2: Camera Stabilization.
    
    Problem: When I move my mouse, the whole world shifts. 
             Computer sees "movement", but I am standing still.
             
    Solution: 
    1. Find distinctive points in the previous frame (corners, edges).
    2. Find where those points went in the current frame (Optical Flow Tracker).
    3. Calculate the rigid body transform (Rotation + Translation) that aligns them.
    4. If we apply the INVERSE of this transform, we "cancel out" the mouse movement.
    """
    
    # 1. Find good features to track (corners are best)
    # maxCorners=200: We don't need thousands, just enough to get a consensus.
    # minDistance=30: Don't pick points too close together.
    prev_pts = cv2.goodFeaturesToTrack(prev_prev_gray := prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30)
    
    # If the screen is black or blur, we might find nothing. Return identity matrix (no change).
    if prev_pts is None:
        return np.eye(2, 3, dtype=np.float32)

    # 2. Calculate sparse optical flow (Lucas-Kanade)
    # This just tells us "Point A at (10,10) moved to (12,11)"
    curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)
    
    # Filter out points that weren't found (status=0)
    good_prev = prev_pts[status==1]
    good_curr = curr_pts[status==1]
    
    if len(good_prev) < 10: 
        # Not enough points to be confident about how the camera moved. 
        # Safer to assume no movement than to guess wildly.
        return np.eye(2, 3, dtype=np.float32)
        
    # 3. Estimate the transformation matrix
    # "estimateAffinePartial2D" is key here. It restricts the solution to 
    # Translation + Rotation + Uniform Scaling (approximated). 
    # It assumes the camera didn't shear or stretch the image, which is true for mouse look.
    m, _ = cv2.estimateAffinePartial2D(good_prev, good_curr)
    
    if m is None:
        return np.eye(2, 3, dtype=np.float32)
        
    # 'm' transforms prev -> curr.
    # To stabilize, we want to know how to warp curr -> prev (to cancel the motion).
    # So we invert it.
    m_inv = cv2.invertAffineTransform(m)
    
    return m_inv

def compute_optical_flow(prev_gray, curr_stabilized_gray):
    """
    Step 3: Dense Optical Flow.
    
    Now that we've (hopefully) stabilized the image, any remaining movement 
    SHOULD be actual player movement (walking/strafing).
    
    We use Farneback's algorithm. It's dense (calculates for every pixel).
    """
    
    # Parameters explained:
    # pyr_scale=0.5:  Build a pyramid half-size at each layer. Handles large motions better.
    # levels=3:       Number of pyramid layers.
    # winsize=15:     Look at a 15x15 window around each pixel. Larger = smoother but blurs edges.
    # iterations=3:   How many times to refine the guess at each level.
    # poly_n=5:       Size of pixel neighborhood to approximate polynomial.
    # poly_sigma=1.2: Smoothness of gaussian.
    
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, 
        curr_stabilized_gray, 
        None, 
        pyr_scale=0.5, 
        levels=3, 
        winsize=15, 
        iterations=3, 
        poly_n=5, 
        poly_sigma=1.2, 
        flags=0
    )
    
    # Flow is a 2D array (dy, dx). We just want "Speed" (Magnitude).
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    
    return mag
