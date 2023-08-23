# ROS Drone Object Detection
An implementation of a vision pipeline for target detection and classification, incorporating a custom-trained CNN model and Holistically-Nested Edge Detection (HED) deep learning model. A working demonstration is shown with ROS and Gazebo. Skip to [Demonstration](#demonstration) to see the pipeline working.

## Table of Contents

- [About](#about)
- [How It Works](#how-it-works)
- [Demonstration](#demonstration)
    - [Install](#install)
    - [Usage](#usage)
    - [Video](#video)
    - [Results](#results)
## About
This project was developed for the Object Detection, Classification, and Localization component of the 2023 SUAS drone competition. The competition drone flies over a section of runway and must detect and classify various targets on the ground by their shape, color, and the letter printed at the center of each target. A series of specific targets with their descriptions are given, and the drone is required to know where they are. 
<p align="center">
    <img src="https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/target_semicirclewhite7.jpg" alt="A 'P' on a yellow semicircle" width=10% height=10%>
    <br>
    A "P" on a yellow semicircle
</p>
Due to hardware constraints, it was hard to capture letters on the target clearly, so we decided to focus on color + shape classification.

## How It Works
Hardware Specs/Constraints
- Camera: Arducam 64MP Hawkeye Motorized Focus Camera Module
- Resolution: 9152 pixels by 6944 pixels, 64MP
- Pixel Size: 0.8 µm x 0.8 µm
- Shutter Speed: Adjustable

Pipeline overview:
<div style="display:flex;">
    <img src="https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/pipeline%20diagram.svg" alt="Pipeline Flowchart" style=" vertical-align: top;">
    
</div>

The architecture of our custom-trained CNN model for shape classification is as follows:

<div style="width: 100%; overflow: auto;">
  <img src="https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/model_arch_diagram.png" style="max-width: 300%; height: auto;">
</div>


## Demonstration
### Install
Install [ROS Noetic](http://wiki.ros.org/noetic/Installation/Ubuntu). Since ROS only runs on Linux, Windows users should install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) before installing ROS.

Clone this repository:
```
git clone https://github.com/shenrunzhang/ROS-Drone-Object-Detection.git
```
Create a shell script to start Arducopter simulation in Gazebo.
```
cd ~
vim startsitl.sh
```
Press i to enter insert mode. Copy and paste the following content into the editor:
```
#!/bin/bash
cd ~/ardupilot/ArduCopter/ && sim_vehicle.py -v ArduCopter -f gazebo-iris --console
```
Press ```Esc``` to exit edit mode and type `:wq` to save and quit. Then make the script executable.  
```
chmod +x startsitl.sh
```
------
To run the demonstration, copy and execute each line in a new terminal:
```
$ roslaunch iq_sim runway.launch         # Opens Gazebo world
$ ./startsitl.sh                         # Run the shell script
$ roslaunch iq_sim apm.launch            # Start MavROS
$ rosrun iq_gnc movement.py              # Start the demo script
```
### Usage
To just use the pipeline, you must first load the target classification model and Holistically-Nested Edge Detection model (HED). `load_models` outputs the shape classification model and HED.
```
from modules import pipeline

classification_model_path = "modules/shape_classification_model_gazebo.h5" # Load shape classification model
prototxt_path = "modules/edgeFinder/deploy.prototxt" # Load edge detection
caffemodel_path = "modules/edgeFinder/hed_pretrained_bsds.caffemodel" # Load edge detection

prob_model, edge_detection_model = load_models(classification_model_path, prototxt_path, caffemodel_path) # Return models
```
Then pass in an aerial image with the shape and edge models to get a list of targets with detected location, shape and color attributes
```
target_list = get_target_list(aerial_image, prob_model, edge_detection_model)
```

### Demo Script Flight Plan
The demo script takes the drone over a 40 m stretch of runway, on which targets have been placed of the specified colors and shapes. The generation of gazebo targets is automated in the script `\src\iq_gnc\scripts\modules\geolocation.py`. Several waypoints have been placed to help guide the drone as it takes pictures of the targets at regular intervals.

![Flight Plan](https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/flight%20plan.PNG)

### Video
<p align="center">
  <a href="https://www.youtube.com/watch?v=liCptHpHUXY" target="_blank">
    <img src="https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/thumbnail.PNG" alt="Your Image Alt Text" width=70% height=90%>
  </a>
</p>

### Results
For each target detected, its global position, shape, and color are shown. Note that the drone starts at x=0, y=0.
<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_0.jpg" alt="Image 1" width="90%">
    <br>
    <p>Image 1. Drone position: x = -0.19 m, y = 6.05 m</p>

</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_1.jpg" alt="Image 2" width="90%">
  <br>
  <p>Image 2. Drone position: x = -0.42 m, y = 12.04 m</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_2.jpg" alt="Image 3" width="90%">
  <br>
  <p>Image 3. Drone position: x = -0.65 m, y = 18.04 m</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_3.jpg" alt="Image 4" width="90%">
  <br>
  <p>Image 4. Drone position: x = -0.86 m, y = 24.01 m</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_4.jpg" alt="Image 5" width="90%">
  <br>
  <p>Image 5. Drone position: x = -1.08 m, y = 29.97 m</p>
</div>







