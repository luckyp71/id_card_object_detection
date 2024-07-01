import os

from detectron2.engine import DefaultPredictor
from dotenv import load_dotenv
from utils.util import get_train_cfg
import cv2
import numpy as np

load_dotenv()

cfg = get_train_cfg(
    config_file_path=os.environ.get('CONFIG_FILE_PATH'),
    checkpoint_url=os.environ.get('CHECKPOINT_URL'),
    train_dataset_name=os.environ.get('TRAIN_DATASET_NAME'),
    output_dir=os.environ.get('OUTPUT_DIR')
)
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7

predictor = DefaultPredictor(cfg)

def detect_id_document(image):
    bboxes = []
    output = predictor(image)['instances']
    if predictor(image)['instances'].pred_boxes.tensor.shape[0] > 1:
        for i in range(len(output.pred_classes.squeeze().cpu().numpy().tolist())):
            if output.pred_classes[i]==0:
                bboxes.append(output.pred_boxes.tensor.squeeze().cpu().numpy()[i].tolist())
    else:
        if output.pred_classes==0:
            bboxes.append(output.pred_boxes.tensor.squeeze().cpu().numpy().tolist())
    return bboxes


def detect_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    threshold=80.0
    is_blurry = variance < threshold
    return is_blurry, variance

def detect_glare(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    glare_ratio = np.sum(threshold == 255)
    threshold = 0.1
    has_glare = glare_ratio > threshold
    return has_glare, glare_ratio

def detect_hologram(image):
    output = predictor(image)
    if 1 in output['instances'].pred_classes.cpu().numpy().tolist():
        return True
    return False