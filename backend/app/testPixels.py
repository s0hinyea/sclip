import cv2
from pathlib import Path
from utils.file_utils import build_paths, save_file


def _mouse_callback(event, x, y, flags, image):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Note: image is BGR; indexing is [row (y), column (x)]
        bgr = image[y, x]
        print(f"Clicked at (x={x}, y={y})  BGR={bgr.tolist()}")

"""
def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    image_path = base_dir / "data" / "image1.png"

    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    normal_image = cv2.resize(image, (1920, 1080))

    window_name = "Image - click to read pixel (BGR)"
    cv2.namedWindow(window_name)

    # Wrap the callback to pass the image as the 'param' argument
    def callback(event, x, y, flags, param):
        _mouse_callback(event, x, y, flags, normal_image)

    cv2.setMouseCallback(window_name, callback)
    cv2.imshow(window_name, normal_image)

    print(normal_image.shape)
    print("Instructions: click anywhere on the image window; press any key to exit.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""



def main(frame_index=None, t_sec=None, target_size=(1920, 1080), window_name="Frame"):
    """
    Open a window showing a specific frame from the video.
    Provide either frame_index (0-based) or t_sec (timestamp in seconds).
    If both are given, frame_index takes precedence.
    """
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    video_path = BASE_DIR/ "data" / "uncapped_MedalTVValorant20250820010551.mp4"
    
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("Error: could not open video")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    if frame_index is None:
        if t_sec is None:
            print("Provide frame_index or t_sec")
            cap.release()
            return False
        try:
            frame_index = int(round(float(t_sec) * fps))
        except Exception:
            print("Invalid t_sec provided")
            cap.release()
            return False

    # Seek and read
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
    ok, frame = cap.read()
    if not ok:
        print(f"Failed to read frame at index {frame_index}")
        cap.release()
        return False

    # Normalize for consistent inspection
    frame = cv2.resize(frame, target_size)

    cv2.namedWindow(window_name)
    
    def callback(event, x, y, flags, param):
        _mouse_callback(event, x, y, flags, frame)

    cv2.setMouseCallback(window_name, callback)
    
    cv2.imshow(window_name, frame)
    print(f"Showing frame_index={frame_index}, fps={fps}")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cap.release()
    return True


if __name__ == "__main__":
    main(264)
