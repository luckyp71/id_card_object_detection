import time
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette import status
from PIL import Image
import numpy as np
import threading
from controllers.id_detection_controller import detect_id_document, detect_blur, detect_glare, detect_hologram
from models.ResponseModel import ResponseModel

id_router = APIRouter(
    prefix="/id_detection",
    tags=["id_detection"]
)

response_model = ResponseModel(response_code=0, data={})

@id_router.post("/analyze")
async def analyze_id_detection(file: List[UploadFile] = File(...)):
    responses = []
    threads = []
    for f in file:
        if f.filename == "":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No file uploaded")

        thread = threading.Thread(target=process_image, args=(responses, f,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Setup response
    response_model.response_code = status.HTTP_200_OK
    response_model.data = responses
    return response_model

def process_image(responses, f):
    time.sleep(1)
    image = Image.open(f.file)
    image_arr = np.array(image)

    bbox = detect_id_document(image_arr)[0]
    x, y, w, h = bbox

    # ID Card Detection
    id_image = image_arr[int(y):int(y) + int(h), int(x):int(x) + int(w)]
    # Blur Detection
    is_blurry, blur_value = detect_blur(id_image)
    # Glare Detection
    has_glare, glare_value = detect_glare(id_image)
    # Hologram Detection
    is_hologram = detect_hologram(id_image)

    responses.append({"blur": {
            "is_blurry": is_blurry.__str__(),
            "value": blur_value},
            "glare": {
                "has_glare": has_glare.__str__(),
                "value": int(glare_value)},
            "hologram": {
                "is_hologram": is_hologram.__str__()
            }
        })