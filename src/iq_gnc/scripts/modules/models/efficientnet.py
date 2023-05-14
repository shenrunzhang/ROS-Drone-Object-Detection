import keras
from keras.applications.mobilenet import MobileNet
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import tensorflow as tf

# Load the MobileNet model
base_model = tf.keras.applications.EfficientNetB7(include_top=False, weights='imagenet', input_shape=(120,120,3))
base_model.trainable = False

# Add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)

# Add a fully connected layer
x = Dense(1024, activation='relu')(x)

# Add a logistic layer
predictions = Dense(13, activation='softmax')(x)

# Compile the model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the layers of the base_model
for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Prepare the data generators
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True,
                                   validation_split=0.2) # split validation set

train_data = train_datagen.flow_from_directory(
    '../training_data/shapes',
    target_size=(120, 120),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_data = train_datagen.flow_from_directory(
    '../training_data/shapes',
    target_size=(120, 120),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Train the model
model.fit(train_data, epochs = 100, validation_data = val_data)
model.save("mobilenet_100epochs.h5")
