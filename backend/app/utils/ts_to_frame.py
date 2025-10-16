def ts_to_frame(timestamp, fps=60.0):
    """
    Convert timestamp to frame number 
    
    Args:
        timestamp (float): Time in seconds
        fps (float): Frames per second (default 60)    
    Returns:
        int: Frame number
    """
    
    frame_number = int(round(float(timestamp) * fps)) - 10
    return max(0, frame_number)  