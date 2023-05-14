import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
import cv2
import re

# Loads model 
model = tf.keras.models.load_model('shenmodel_2.h5')

# Folder where imgs you want to predict on are located
source_folder = 'targets/'

# List of class names
class_names = ['circle', 'cross', 'heptagon', 'hexagon', 'octagon', 'pentagon', 
               'quartercircle', 'rectangle', 'semicircle', 'square', 'star', 'trapezoid', 'triangle']

# Defines function to sort alphanumerically
#  -> 1, 4, 7, 11, 15, ... not 1, 11, 15, 4, 7, ...
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

# Gets list of paths from folder, sorts them
files = sorted_alphanumeric(os.listdir(source_folder))
actual = ["trapezoid", "triangle", "heptagon", "semicircle", "rectangle", "cross", "quartercircle", "cross", "circle", "triangle"]

# Loads each image as an array and appends to a list
images = []
for img in files:
    img = tf.keras.preprocessing.image.load_img(source_folder + img, target_size=(120, 120))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    images.append(img)

# Convert the list of images to an array to be fed into model
images = np.vstack(images)

# Set up model
probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

# Make predictions, each prediction is a list of probabilities (must select highest prob)
predictions = probability_model.predict(images)

# Convert predictions into class names
guesses = [class_names[np.argmax(prediction)] for prediction in predictions]


print(list(zip(guesses, actual)))
amt_right = 0
for i in range(len(guesses)):
    if guesses[i] == actual[i]:
        amt_right += 1
print(str(amt_right) + "/" + str(len(guesses)))
