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
from modules.geolocation import pixel_to_loc


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
        print("edge case ")
    if (newuppery - newlowery > 128):
        print("edge case ")
    print("COORDINATES")
    print(str(newlowerx) + " , " + str(newupperx) + " , " + str(newlowery) + " , " + str(newupperx))
    return newlowerx, newupperx, newlowery, newuppery

def filter_targets(target_list, displacement_threshold=1):
    lst = []
    
    for target in target_list:
        pos1 = target.get_real_pos()
        unique = True
        for target_2 in lst:
            pos2 = target_2.get_real_pos()
            displacement = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5 
            if displacement < displacement_threshold:
                unique = False
                break
        
        if unique:
            lst.append(target)
            
    return lst
                
        
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
def load_models(model_path: str) -> any:
    '''
    Keeps the classfication and HED model loaded, to be run before get_target_list
    input: 
    model_path - path to the classification model
    output:
    classification model 
    HED model
    '''
    
    # load model
    model = tf.keras.models.load_model(model_path)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    
    # Holistically nested Edge Detection stuff
    prototxt_path = "vision/modules/edgeFinder/deploy.prototxt"
    caffemodel_path = "vision/modules/edgeFinder/hed_pretrained_bsds.caffemodel"

    # Load HED model (doing this outside inference.predict() keeps model loaded)
    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
    cv2.dnn_registerLayer('Crop', inference.CropLayer)

    
    return probability_model, net
    
def get_target_list(image, probability_model, edge_detection_model)-> list:
    '''
    input: aerial image, classification model, HED model
    output: list of target objects
    '''
    # TODO: Account for last tile
    

    # List of class names for model
    class_names = ['circle', 'cross', 'heptagon', 'hexagon', 'octagon', 'pentagon', 
               'quartercircle', 'rectangle', 'semicircle', 'square', 'star', 'trapezoid', 'triangle']

    # print("flag D")
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
            pred = inference.predict(tile, edge_detection_model, width=tile_width, height=tile_height)
            
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
    
    classification_model_path = 'shape_classification_model_gazebo.h5'
    
    # Load aerial images pic0.jpg - pic4.jpg
    aerial_images = []
    # Drone locations in real world coordinates when each picture was taken
    drone_pos = [[-0.19, 6.05], [-0.42, 12.04], [-0.65, 18.04], [-0.86, 24.01], [-1.08, 29.97]]

    for i in range(5):
        img = cv2.imread(r"C:\Users\Shen\Documents\GitHub\RiceUAV\pic{}.jpg".format(i))
        aerial_images.append([img, drone_pos[i][0], drone_pos[i][1]])
        
    # load the classification model
    
    prob_model, edge_detection_model = load_models(classification_model_path)

    # iterate through the images and classify all the targets
    global_target_list = []
    
    for index in range(len(aerial_images)):
        print("Working on aerial image {}".format(index))
        aerial_image, drone_x, drone_y = aerial_images[index]
        target_list = get_target_list(aerial_image, prob_model, edge_detection_model)
        print("number of targets: ",len(target_list))        

        for i in range(len(target_list)):
            targ = target_list[i]
            # # ensures a unique filename
            # filename = "target_" + str(i) + targ.get_shape() + targ.get_color() + ".jpg"
            # cv2.imwrite(filename, targ.get_image())
            
            px, py = targ.get_pixel_pos()
            image_width = 2560
            image_height = 1440
            
            # Draw bbox around target on image, and include coordinates
            targ_x, targ_y = pixel_to_loc(px, image_height - py, drone_x, drone_y, 20, image_height, image_width, H_fov=1.0472)
            
            # Add real coordinates to target
            targ.set_real_pos(targ_x, targ_y)
            
            bb_color = (72, 250, 223)
            x, y = targ.get_x(), targ.get_y()
            cv2.rectangle(aerial_image, (x - 60, y - 60), (x + 60, y + 60), bb_color, 4)
            
            # print position
            cv2.putText(aerial_image, 
                        "x: {}, y: {}".format(targ_x, targ_y),
                        (x + 65, y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        bb_color,
                        2,
                        cv2.LINE_AA)
            
            # print target color
            cv2.putText(aerial_image, 
                        "color: {}".format(targ.get_color()),
                        (x + 65, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        bb_color,
                        2,
                        cv2.LINE_AA)
            
            # print target shape
            cv2.putText(aerial_image, 
                        "shape: {}".format(targ.get_shape()),
                        (x + 65, y + 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        bb_color,
                        2,
                        cv2.LINE_AA)
        
        # save aerial image
        filename = "aerial_image_processed_{}.jpg".format(index)
        cv2.imwrite(filename, aerial_image)
        
        # ----------------------------------------------------------------
        
        global_target_list += target_list
        
    # save all individual targets
    print(global_target_list)
    print(len(global_target_list))
    global_target_list = filter_targets(global_target_list)
    for i in range(len(global_target_list)):
        print(i)
        target = global_target_list[i]
        
        filename = "res_filtered/" + target.get_shape() + "_" + target.get_color() + "_" + str(i) + ".jpg"
        
        cv2.imwrite(filename, target.get_image())
        
        
        
    
    
