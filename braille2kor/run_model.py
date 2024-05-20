import PIL
from ultralytics import YOLO
#from convert import convert_to_braille_unicode, parse_xywh_and_class
import json
import numpy as np
import torch
from BrailleToKorean.BrailleToKor import BrailleToKor


def convert_to_braille_unicode(str_input: str, path: str = "./utils/braille_map.json") -> str:
    with open(path, "r", encoding="utf-8") as fl:
        data = json.load(fl)

    if str_input in data.keys():
        str_output = data[str_input]
    return str_output



def parse_xywh_and_class(boxes: torch.Tensor) -> list:
    """
    boxes input tensor
        boxes (torch.Tensor) or (numpy.ndarray): A tensor or numpy array containing the detection boxes,
            with shape (num_boxes, 6).
        orig_shape (torch.Tensor) or (numpy.ndarray): Original image size, in the format (height, width).
    Properties:
        xyxy (torch.Tensor) or (numpy.ndarray): The boxes in xyxy format.
        conf (torch.Tensor) or (numpy.ndarray): The confidence values of the boxes.
        cls (torch.Tensor) or (numpy.ndarray): The class values of the boxes.
        xywh (torch.Tensor) or (numpy.ndarray): The boxes in xywh format.
        xyxyn (torch.Tensor) or (numpy.ndarray): The boxes in xyxy format normalized by original image size.
        xywhn (torch.Tensor) or (numpy.ndarray): The boxes in xywh format normalized by original image size.
    """

    # copy values from troublesome "boxes" object to numpy array
    new_boxes = np.zeros(boxes.shape)
    new_boxes[:, :4] = boxes.xywh.cpu().numpy()  # Move tensor to CPU and then convert to NumPy
    new_boxes[:, 4] = boxes.conf.cpu().numpy()   # Move tensor to CPU and then convert to NumPy
    new_boxes[:, 5] = boxes.cls.cpu().numpy()    # Move tensor to CPU and then convert to NumPy


    # sort according to y coordinate
    new_boxes = new_boxes[new_boxes[:, 1].argsort()]

    # find threshold index to break the line
    y_threshold = np.mean(new_boxes[:, 3]) // 2
    boxes_diff = np.diff(new_boxes[:, 1])
    threshold_index = np.where(boxes_diff > y_threshold)[0]

    # cluster according to threshold_index
    boxes_clustered = np.split(new_boxes, threshold_index + 1)
    boxes_return = []
    for cluster in boxes_clustered:
        # sort according to x coordinate
        cluster = cluster[cluster[:, 0].argsort()]
        boxes_return.append(cluster)

    return boxes_return

def load_model(model_path):
    """load model from path"""
    model = YOLO(model_path)
    return model

def load_image(image_path):
    """load image from path"""
    image = PIL.Image.open(image_path)
    return image
'''
# constants
CONF = 0.15 # or other desirable confidence threshold level
MODEL_PATH = "./models/yolov8_braille.pt"
IMAGE_PATH = "images/kaka3.jpg"

# receiving results from the model
image = load_image(IMAGE_PATH)
model = YOLO(MODEL_PATH)
res = model.predict(image, save=True, save_txt=True, exist_ok=True, conf=CONF)
boxes = res[0].boxes  # first image
list_boxes = parse_xywh_and_class(boxes)

result = ""
for box_line in list_boxes:
    str_left_to_right = ""
    box_classes = box_line[:, -1]
    for each_class in box_classes:
        str_left_to_right += convert_to_braille_unicode(model.names[int(each_class)])
    result += str_left_to_right + "\n"

print(result)
b = BrailleToKor()
print(b.translation(result))
'''