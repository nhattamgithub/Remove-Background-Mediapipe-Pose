
import numpy as np
import cv2
import glob
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

videos = glob.glob('D:/ConDuongHocVan/Python/NLN/input/videos/*.mp4')
cap0 = cv2.VideoCapture(videos[0])
cap1 = cv2.VideoCapture(videos[1])


background_path = ('D:/ConDuongHocVan/Python/NLN/input/background_imgs/bg.jpg') # 1920 x 1080
background = cv2.imread(background_path)

position = np.array([[50,50],[200,200]])
scale_percent = [60,70]
image_array = []
with mp_pose.Pose(
    enable_segmentation = True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while True:
        s0, frame0 = cap0.read()
        s1, frame1 = cap1.read()
        if s1:
            f1 =  add_pixel(frame1,scale_percent[1],position[1],background)

            try:
                f0 =  add_pixel(frame0,scale_percent[0],position[0],background)
                # pose:
                f1.flags.writeable = False
                f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2RGB)
                results = pose.process(f1)
                f1.flags.writeable = True
                f1 = cv2.cvtColor(f1, cv2.COLOR_RGB2BGR)
                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
                f1 = np.where(condition, f1, background)

                final = mppose.removeBG(f0, f1)

            except (TypeError,AttributeError):
                if not s0:
                    f1.flags.writeable = False
                    f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2RGB)
                    results = pose.process(f1)
                    f1.flags.writeable = True
                    f1 = cv2.cvtColor(f1, cv2.COLOR_RGB2BGR)
                    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5
                    final = np.where(condition, f1, background)
                else:
                    final = mppose.removeBG(f0, f1)

            finally:
                cv2.imshow('add background', final)
                height, width, layers = final.shape
                size = (width,height)
                image_array.append(final)
            

        if cv2.waitKey(1) & 0xFF == ord('q'): # hit Q to stop playing video:
            break
    out = cv2.VideoWriter('D:/ConDuongHocVan/Python/NLN/output/r1.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 24, size)
    for i in range(len(image_array)):
        out.write(image_array[i])
    out.release()
cv2.destroyAllWindows()