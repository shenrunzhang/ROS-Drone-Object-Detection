import cv2
from target import Target
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import classify_targets
from edgeFinder import inference
import target
    
def resize_img(img, resize_factor):
    new_h, new_w = img.shape[:2]
    new_shape = (new_w // resize_factor, new_h // resize_factor)

    resized_img = cv2.resize(img, new_shape, interpolation= cv2.INTER_LINEAR)

    return resized_img

#if __name__ == "__main__":
LOCATION = r"C:\Users\Shen\Documents\GitHub\RiceUAV\vision\modules\testimg\sshtesthigh5.jpg"
prototxt_path = "vision/modules/edgeFinder/deploy.prototxt"
caffemodel_path = "vision/modules/edgeFinder/hed_pretrained_bsds.caffemodel"

# Load model (doing this outside inference.predict() keeps model loaded)
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
cv2.dnn_registerLayer('Crop', inference.CropLayer)

frame1 = cv2.imread(LOCATION)
cropped = frame1[1000:2500, 3000:6000] # 1500, 3000

global_height = cropped.shape[0]
global_width = cropped.shape[1]

size_factor = 2

tile_height = global_height//size_factor
tile_width = global_width//size_factor
global_target_list = []
for row in range(size_factor):
    for col in range(size_factor):
        
        lowerR = (row)*tile_height
        upperR = (row+1)*tile_height
        lowerC = (col)*tile_width
        upperC = (col+1)*tile_width
        
        tile = cropped[lowerR:upperR,lowerC:upperC]
        
        # inference result returns a grayscale image
        pred = inference.predict(tile, net, width=tile_width, height=tile_height)
        
        (thresh, pred) = cv2.threshold(pred, 50, 255, cv2.THRESH_BINARY)

        # Finds targets
        target_lst = classify_targets.find_targets(pred)


        # Draws bboxes onto original image
        for index, target in enumerate(target_lst):
            x, y, w, h = target.get_bbox()
            #cv2.imshow("target%d" % index, target_tile)
            #cv2.rectangle(tile, (x, y), (x + w, y + h), (255, 0, 0), 4)
            c_x = target.get_x()
            c_y = target.get_y()
            
            lower_y =  max(c_y - 60 + row * tile_height,0)
            upper_y = min(c_y+60 + row * tile_height, cropped.shape[0])
            lower_x = max(c_x-60 + col * tile_width, 0)
            upper_x = min(c_x+60 + col * tile_width, cropped.shape[1])
            
            print(lower_y,upper_y,lower_x,upper_x)
            
            x += col * tile_width
            y += row * tile_height       
            
            target_tile = cropped[lower_y:upper_y,lower_x:upper_x].copy()
            
            global_target_list.append(Target(target_tile, x + w // 2, y + h // 2, (x, y, w, h)))
            
            
        
for index, target in enumerate(global_target_list):
    cv2.imwrite("target%d.jpg"%index, target._image)


