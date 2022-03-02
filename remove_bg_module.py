import cv2
import mediapipe as mp
from mediapipe_pose_module import mpPose

mppose = mpPose()
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def resize(frame, scale_percent):
    fixed_height = int(frame.shape[0] * scale_percent / 100)
    height_percent = (fixed_height / float(frame.shape[0]))
    width_size = int((float(frame.shape[1]) * float(height_percent)))
    dim = (width_size, fixed_height)
    resized_frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return resized_frame



def add_pixel(frame,scale_percent,position,background):
    color = [255, 255, 255]
    resized_frame = resize(frame, scale_percent)
    added_pixel_img = cv2.copyMakeBorder(resized_frame, position[1], background.shape[0] - resized_frame.shape[0] - position[1] , 
                    position[0], background.shape[1] - resized_frame.shape[1] - position[0], cv2.BORDER_CONSTANT, value=color)   
    return added_pixel_img

scale_percent=60
position=[50,50]

def remove_bg(frame, background):
    with mp_pose.Pose(
    enable_segmentation = True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
        f= add_pixel(frame,scale_percent,position,background)
        final = mppose.removeBG(f, background)
        return final