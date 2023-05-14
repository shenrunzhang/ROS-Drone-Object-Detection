import argparse
import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
import cv2
import re
from modules.edgeFinder import inference
from modules.classify_targets import find_targets
from modules.target import Target
from modules.color import classify_color


def get_best_img(lowerx, upperx, lowery, uppery, maxx, maxy):
    if ((upperx - lowerx) > 128):
        width = upperx - lowerx
        newlowerx = max(lowerx + (width - 128) // 2, 0)
        newupperx = min(upperx - (width - 128) // 2, maxx)
        # choose middle 128
    if ((upperx - lowerx) <= 128):
        width = upperx - lowerx 
        newlowerx = max(lowerx - (128 - width) // 2, 0)
        newupperx = min(upperx + (128 - width) //2, maxx)
    if ((uppery - lowery) > 128):
        height = uppery - lowery
        newlowery = max(lowery + (height - 128) // 2, 0)
        newuppery = min(uppery - (height - 128) // 2, maxy)
        # choose middle 128
    if ((upperx - lowerx) <= 128):
        height = uppery - lowery
        newlowery = max(lowery - (128 - height) // 2, 0)
        newuppery = min(uppery + (128 - height) // 2, maxy)
    if (newupperx - newlowerx > 128):
        print("edge case fuck")
    if (newuppery - newlowery > 128):
        print("edge case fuck")
    print("COORDINATES JUST DROPPED")
    print(str(newlowerx) + " , " + str(newupperx) + " , " + str(newlowery) + " , " + str(newupperx))
    return newlowerx, newupperx, newlowery, newuppery
"""
Pipeline:
Image -> Detect Targets -> Classify Shape -> Classify Color -> 
Output: List<(TopLeft, BottomRight, Shape, Color)>

Global Target List = []
Load Image -> Split image into tiles:
For each tile in tiles:
    edge detect using HED
    targets = get shapes from each tile using find_targets
    Run inference on each target:
        write each target to an image then add that image to images???? Seems inefficient
        can you just do tf.keras.preprocessing.iamge.img_to_array(target.image)??
        images = []
        for img in files:
            img = tf.keras.preprocessing.image.load_img(source_folder + img, target_size=(128, 128))
            img = tf.keras.preprocessing.image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            images.append(img)

        # Convert the list of images to an array to be fed into model
        images = np.vstack(images)

        # Set up model
        probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

        # Make predictions, each prediction is a list of probabilities (must select highest prob)
        predictions = probability_model.predict(images, batch_size=10)

        # Convert predictions into class names
        guesses = [class_names[np.argmax(prediction)] for prediction in predictions]

"""
def get_target_list(image)-> list:
    '''
    input: aerial image
    output: list of target objects
    '''
    
    # load model
    model = tf.keras.models.load_model('shapemodel.h5')
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    # List of class names for model
    class_names = ['circle', 'cross', 'heptagon', 'hexagon', 'octagon', 'pentagon', 
               'quartercircle', 'rectangle', 'semicircle', 'square', 'star', 'trapezoid', 'triangle']

    
    # Holistically nested Edge Detection stuff
    prototxt_path = "modules/edgeFinder/deploy.prototxt"
    caffemodel_path = "modules/edgeFinder/hed_pretrained_bsds.caffemodel"

    # Load HED model (doing this outside inference.predict() keeps model loaded)
    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
    cv2.dnn_registerLayer('Crop', inference.CropLayer)

    global_height = image.shape[0]
    global_width = image.shape[1]
    
    size_factor = 1

    tile_height = global_height//size_factor
    tile_width = global_width//size_factor
    
    global_target_list = []
    for row in range(size_factor):
        for col in range(size_factor):
        
            lowerR = (row)*tile_height
            upperR = (row+1)*tile_height
            lowerC = (col)*tile_width
            upperC = (col+1)*tile_width
            
            
            tile = image[lowerR:upperR,lowerC:upperC]
            
            # inference result returns a grayscale image
            pred = inference.predict(tile, net, width=tile_width, height=tile_height)
            
            (thresh, pred) = cv2.threshold(pred, 50, 255, cv2.THRESH_BINARY)

            # Finds targets
            target_lst = find_targets(pred)
            i = 0
            for target in target_lst:
                cv2.imwrite("targ" + str(i) + ".jpg", target.get_image())
                i += 1


            # Draws bboxes onto original image
            for index, target in enumerate(target_lst):
                x, y, w, h = target.get_bbox()
                c_x = target.get_x()
                c_y = target.get_y()
                
                lower_y =  max(c_y - 60 + row * tile_height,0)
                upper_y = min(c_y + 60 + row * tile_height, image.shape[0])
                lower_x = max(c_x - 60 + col * tile_width, 0)
                upper_x = min(c_x + 60 + col * tile_width, image.shape[1])
                
                target_tile = image[lower_y:upper_y, lower_x:upper_x]
                
                if (target_tile.shape[0] == 0 or target_tile.shape[1] == 0):
                    continue
                target_tile = cv2.resize(target_tile, (120,120))
                
                img = np.expand_dims(target_tile, axis=0)
                prediction = probability_model.predict(img)
                target_shape = class_names[np.argmax(prediction)]
                #  use bounding box for color 
                target_color = classify_color(target_tile).split(':')[0]
                global_target_list.append(Target(target_tile, x + w // 2, y + h // 2, (x, y, w, h), target_shape, target_color))
    
    return global_target_list
    
        
if __name__ == "__main__":
    
    target_list = get_target_list(r"C:\Users\Shen\Documents\GitHub\RiceUAV\croppedtest2.jpg")

    for i in range(len(target_list)):
        targ = target_list[i]
        # ensures a unique filename
        filename = "target_" + str(i) + targ.get_shape() + targ.get_color() + ".jpg"
        cv2.imwrite(filename, targ.get_image())
