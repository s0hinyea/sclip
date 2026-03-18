import sys
import os
import cv2
import numpy as np

# Ensure we can import from our app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.movement.processing import downscale_and_mask, stabilize_frame, compute_optical_flow

def test_phase1_visuals(video_path, output_dir):
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # We'll process just 5 seconds (approx 300 frames) to be quick
    frames_to_process = 300
    
    # Setup Output Video writers
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # 1. Stabilization Debug Video (Side by Side: Raw vs Stabilized)
    # Output width is duplicate (2x) because side-by-side
    stab_out_path = os.path.join(output_dir, "debug_stabilization.mp4")
    # Note: Using 640 as approx width, height is 360
    # Wait, let's get actual dims from first frame
    ret, first_frame = cap.read()
    if not ret: return
    
    first_small, _, _ = downscale_and_mask(first_frame)
    h, w = first_small.shape[:2]
    
    stab_writer = cv2.VideoWriter(stab_out_path, fourcc, fps, (w * 2, h))
    
    # 2. Flow Heatmap Video
    flow_out_path = os.path.join(output_dir, "debug_flow.mp4")
    flow_writer = cv2.VideoWriter(flow_out_path, fourcc, fps, (w, h))

    # Reset
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    prev_gray = None
    
    print(f"Processing {frames_to_process} frames for debug visuals...")
    print(f"Dimensions: {w}x{h}")
    
    for i in range(frames_to_process):
        ret, frame = cap.read()
        if not ret: break
        
        # --- Step 1: Pre-process ---
        curr_small, mask, masked_vis = downscale_and_mask(frame)
        curr_gray = cv2.cvtColor(curr_small, cv2.COLOR_BGR2GRAY)
        
        # Save a single masked frame for sanity check
        if i == 30: # arbitrary frame
            cv2.imwrite(os.path.join(output_dir, "debug_masked.jpg"), masked_vis)
        
        if prev_gray is None:
            prev_gray = curr_gray
            continue
            
        # --- Step 2: Stabilization ---
        # Get transform to align PREV to CURR (or vice versa? Logic check!)
        # Our function returns m_inv, which aligns CURR -> PREV.
        transform = stabilize_frame(prev_gray, curr_gray)
        
        # Warp the CURRENT frame to look like the PREVIOUS frame
        stabilized_curr = cv2.warpAffine(curr_gray, transform, (w, h))
        
        # Visualize Stabilization
        # We need stabilized color frame for the video
        vis_stab_curr = cv2.warpAffine(curr_small, transform, (w, h))
        
        # Combine Side-by-Side
        combined = np.hstack((curr_small, vis_stab_curr))
        stab_writer.write(combined)
        
        # --- Step 3: Optical Flow ---
        mag = compute_optical_flow(prev_gray, stabilized_curr)
        
        # Visualize Flow (Normalize 0-5 motion to 0-255 pixel value for visibility)
        # Any motion > 5 pixels per frame is wildly fast, so capping at 5 is fine for vis.
        vis_flow = np.clip(mag * (255.0 / 5.0), 0, 255).astype(np.uint8)
        
        # Apply strict mask to flow
        vis_flow_masked = cv2.bitwise_and(vis_flow, vis_flow, mask=mask)
        
        # Color map for prettiness
        heatmap = cv2.applyColorMap(vis_flow_masked, cv2.COLORMAP_JET)
        flow_writer.write(heatmap)
        
        prev_gray = curr_gray
        
        if i % 50 == 0:
            print(f"Frame {i}...")

    cap.release()
    stab_writer.release()
    flow_writer.release()
    print("Done! Check the output directory.")

if __name__ == "__main__":
    # Use specific video
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    target_video = os.path.join(data_dir, "uncapped_MedalTVValorant20250820010551.mp4")
    
    if os.path.exists(target_video):
        test_phase1_visuals(target_video, data_dir)
    else:
        print(f"Video not found: {target_video}")

