import cv2
import numpy as np
from pathlib import Path
import cv2

CUT_PIXEL_FRACTION = 0.01

def compute_brightness_contrast(video_path, sample_rate=1):
    """
    Sample frames every `sample_rate` seconds.
    Returns dict with brightness_mean and contrast_mean.
    """
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = total_frames / fps if fps else 0

    brightness_vals = []
    contrast_vals = []
    frame_id = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        time_sec = frame_id / fps
        if time_sec % sample_rate < (1.0/fps):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness_vals.append(float(np.mean(gray)))
            contrast_vals.append(float(np.std(gray)))
        frame_id += 1
    cap.release()
    return {
        "brightness_mean": float(np.mean(brightness_vals)) if brightness_vals else 0.0,
        "contrast_mean":   float(np.mean(contrast_vals)) if contrast_vals else 0.0,
    }


def compute_scene_rate(video_path: Path) -> dict:
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 1.0
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0

    # Figure out frame size so we know how many pixels are in it
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_pixels = width * height

    # Now compute the absolute cut threshold
    some_threshold = int(total_pixels * CUT_PIXEL_FRACTION)

    # Scene-cut detection
    ret, prev_frame = cap.read()
    cuts = 0
    while ret:
        ret, frame = cap.read()
        if not ret:
            break

        gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray_curr = cv2.cvtColor(frame,      cv2.COLOR_BGR2GRAY)
        diff       = cv2.absdiff(gray_curr,  gray_prev)
        non_zero   = cv2.countNonZero(diff)

        if non_zero > some_threshold:
            cuts += 1

        prev_frame = frame

    duration = (total_frames / fps) if fps > 0 else 1
    cap.release()

    return {"scene_rate": cuts / duration if duration > 0 else 0}
