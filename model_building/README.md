# Model Building

### Introduction
Use cases:
- Detect ID Card object based on image
- Detect Hologram of ID Card object based on image
<br/>

While we can build separate models for each task above, but the use case is same i.e. object detection.<br/>
So in this opportunity, I built one model which able to detect both ID Card and/or Hologram of ID Card.<br/><br/>

I used Detectron2 framework to build the model, using transfer-learning approach from pre-trained Faster R-CNN with FPN backbone model (R50-FPN).<br/>
Since I don't get the available data which is ready to use (ID Card images along with the annotations I need),<br/>
so I retrieved the data (images) from google directly and annotated them using Labelme. <br/>
There are around 200 data used to build the model.<br/><br/>

### Prerequisites
Activate python / conda virtual environment, then execute the following commands:
- pip install labelme
- python -m pip install pyyaml==5.3
- python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

### Convert Labelme to COCO Format
Since I annotated the images using labelme, but the model requires COCO data format, <br/>
hence converting the data format (from labelme into COCO) is needed.<br/>
Execute the following command to install labelme2coco:
- pip install -U labelme2coco
<br/>
Navigate to the data directory:
- cd ./data/all_data
<br/>
Split the data into 80% train and 20% test:
- labelme2coco ./ --train_split_rate 0.8 --category_id_start 1

<br/>
After the steps above complete, please kindly check the jupyter lab (model_building.ipynb) file for the modeling steps.<br/>
I split the output model into 10 zip files, since size exceeds github limit (100MB).<br/>
These model files are saved in /model/model_final.zip.001 to model_final.zip.010<br/>
To load the model:<br/>
If you use Windows, select these 10 zip files then right click, select show more option -> 7 zip -> Extract Here