import librosa 
import numpy as np

# Lower = more sensitive (catches more candidates). 
# Since visual handles precision, audio just needs to be a wide net.
RMS_THRESHOLD_MULTIPLIER = 1.2

def find_peaks(audio_data, sample_rate):
    """
    Detect loud moments using RMS energy thresholding.
    Returns a list of (timestamp_seconds, rms_energy) tuples.
    """
    try:
        print("Using RMS energy detection...")
        
        rms = librosa.feature.rms(y=audio_data, frame_length=2048, hop_length=512)[0]
        
        avg_rms = np.mean(rms)
        threshold = avg_rms * RMS_THRESHOLD_MULTIPLIER
        
        results = []
        for i, energy in enumerate(rms):
            if energy >= threshold:
                # Convert RMS frame index to timestamp
                sample_num = i * 512
                timestamp = sample_num / sample_rate
                results.append((timestamp, float(energy)))
        
        print(f"RMS detection: {len(results)} candidates (threshold={threshold:.4f}, avg={avg_rms:.4f})")
        return results
        
    except Exception as e:
        print(f"Error in RMS detection: {e}")
        return []