# ID Card Detection API

### Introduction
This API invokes the final model of ID Card detection.<br/>
Please check the documentation on Swagger for the detail.<br/>
The Swagger documentation can be found in http://localhost:8000/docs
<br/><br/>
### Prerequisites
Activate python / conda virtual environment, then execute the following commands:
- pip install fastapi
- pip install uvicorn
- pip install pydantic
<br/><br/>

#### API Endpoints
There is only one enpoint for this API which can be found in:<br/>
http://localhost:8000/id_detection/analyze<br/>
This endpoint is to analyzes the uploaded image and provides information regarding blurriness, glare, and the presence of hologram on an ID Card.<br/>
This endpoint uses the HTTP Post method with form-data file as its parameter.
<br/><br/>

#### Steps to run
- Please take the model from model_building/model directory and put it inside dl_models
- Navigate to ID Card Detection API root directory then execute **python ./main.py**