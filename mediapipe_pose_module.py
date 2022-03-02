import cv2
import mediapipe as mp
import numpy as np

class mpPose():
  def __init__(self, mode=False,
               enable_seg=True,
               detectionCon=0.5 , trackCon=0.5):
    self.mode = mode
    self.enable_seg = enable_seg
    self.detectionCon = detectionCon
    self.trackCon = trackCon
    self.mpDraw = mp.solutions.drawing_utils
    self.mpPose = mp.solutions.pose
    self.pose = self.mpPose.Pose(static_image_mode=self.mode, 
                                enable_segmentation = self.enable_seg,
                                min_detection_confidence=self.detectionCon,
                                min_tracking_confidence=self.trackCon)

  def removeBG(self, img, imgBg):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = self.pose.process(imgRGB)
    condition = np.stack(
       (results.segmentation_mask,)*3, axis=-1)>0.1
    imgOut = np.where(condition, img, imgBg)
    return imgOut
    
 