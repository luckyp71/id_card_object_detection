import urllib.parse

from PIL import Image
import numpy as np
import pytest
from controllers.id_detection_controller import detect_id_document, detect_blur, detect_glare, detect_hologram
from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app)

@pytest.fixture
def default_doc_id():
    # Image which contains id card's hologram
    image = Image.open('assets/sample_id_card_1.jpg')
    img = np.array(image)
    bbox = detect_id_document(img)[0]
    x, y, w, h = bbox
    id_image = img[int(y):int(y) + int(h), int(x):int(x) + int(w)]
    return bbox, id_image

def test_detect_id_document(default_doc_id):
    assert default_doc_id[0] == [290.9386291503906, 263.0329895019531, 714.7088012695312, 528.2940063476562]

def test_detect_blur(default_doc_id):
     assert detect_blur(default_doc_id[1])[0] == False
     assert detect_blur(default_doc_id[1])[1] == 213.70761291465712

def test_detect_glare(default_doc_id):
    assert detect_glare(default_doc_id[1])[0] == False
    assert detect_glare(default_doc_id[1])[1] == 0

def test_detect_hologram(default_doc_id):
    assert detect_hologram(default_doc_id[1]) == True

def test_analyze_id_detection():
    response = client.post('/id_detection/analyze', data={"file":"assets/sample_id_card_1.jpg"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY