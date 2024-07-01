import os
from typing import List
from fastapi import APIRouter, UploadFile, File
from starlette import status

from controller.id_detection_controller import detect_id_document, detect_blur, detect_glare, detect_hologram
from models.ResponseModel import ResponseModel
from PIL import Image
import numpy as np


id_router = APIRouter(
    prefix="/id_detection",
    tags=["id_detection"]
)

response_model = ResponseModel(response_code=0, data={})

@id_router.post("/analyze")
async def analyze_id_detection(file: List[UploadFile] = File(...)):
    responses=[]
    for i in file:
        image = Image.open(i.file)
        image_arr = np.array(image)

        bbox = detect_id_document(image_arr)[0]
        x, y, w, h = bbox

        # ID Card Detection
        id_image = image_arr[int(y):int(y)+int(h), int(x):int(x)+int(w)]
        # Blur Detection
        is_blurry, blur_value = detect_blur(id_image)
        # Glare Detection
        has_glare, glare_value = detect_glare(id_image)
        # Hologram Detection
        is_hologram = detect_hologram(id_image)
        # Setup response
        responses.append(
                        {"blur":{
                                "is_blurry": is_blurry.__str__(),
                                "value": blur_value},
                           "glare": {
                               "has_glare": has_glare.__str__(),
                                "value": int(glare_value)},
                            "hologram": {
                                "is_hologram": is_hologram.__str__()
                            }
                            })
    response_model.response_code = status.HTTP_200_OK
    response_model.data = responses
    return response_model

