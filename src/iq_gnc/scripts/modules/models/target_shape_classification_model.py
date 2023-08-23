import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import pathlib
import matplotlib.pyplot as plt
import cv2

MODEL_SAVE_PATH = 'shenmodel_3.h5'

num_epochs = 200

# Load data
data_dir = pathlib.Path(r"training_data\shapes")

batch_size = 32
img_height = 120
img_width = 120

# train/val split 
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)
val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# get class names
class_names = train_ds.class_names
print(class_names)

# Normalization and batching
normalization_layer = tf.keras.layers.Rescaling(1./255)
normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
num_classes = len(class_names)

# Create Model
model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255),
  # first convo layer
  tf.keras.layers.Conv2D(filters=8, kernel_size = (5,5), padding="same",activation="relu"),
  # second convo layer
  tf.keras.layers.Conv2D(filters = 16, kernel_size = (3,3), padding="same",activation = 'relu'),
  tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides=(2,2)),
  tf.keras.layers.Dropout(rate = 0.2),
  # third convo layer
  tf.keras.layers.Conv2D(filters = 32, kernel_size = (3, 3), padding="same", activation = 'relu'),
  # fourth convo layer
  tf.keras.layers.Conv2D(filters = 32, kernel_size = (3, 3), padding="same", activation = 'relu'),
  tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides=(2,2)),
  tf.keras.layers.Dropout(rate = 0.2),
  # fifth convo layer
  tf.keras.layers.Conv2D(filters = 32, kernel_size = (3, 3), padding="same", activation = 'relu'),
  tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides=(2,2)),
  tf.keras.layers.Dropout(rate = 0.2),
  # sixth convo layer
  tf.keras.layers.Conv2D(filters = 16, kernel_size = (3, 3), padding="same", activation = 'relu'),  
  # seventh convo layer
  tf.keras.layers.Conv2D(filters = 8, kernel_size = (3, 3), padding="same", activation = 'relu'),
  tf.keras.layers.MaxPooling2D(pool_size = (2, 2), strides=(2,2)),
  tf.keras.layers.Dropout(rate = 0.2),
  # flatten
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(units = 64, activation = 'relu'),
  tf.keras.layers.Dropout(rate = 0.5),
  tf.keras.layers.Dense(units = num_classes, activation = 'softmax')
])

model.compile(
  optimizer='adam',
  loss='sparse_categorical_crossentropy',
  metrics=['accuracy'])

# Train model
model.fit(
  train_ds,
  validation_data=val_ds,
  epochs= num_epochs
)

model.save(MODEL_SAVE_PATH)

# no tuning: accuracy after 100 epochs 0.8323
# tuning: seven layers after 100 epoch 0.9569
