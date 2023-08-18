# ROS Drone Object Detection
An implementation of a vision pipeline for target detection and classification, incorporating a custom-trained CNN model and Holistically-Nested Edge Detection (HED) deep learning model. A working demonstration is shown with ROS and Gazebo. Skip to [Demonstration](#demonstration) to see the pipeline working.

## Table of Contents

- [About](#about)
- [How It Works](#how-it-works)
- [Demonstration](#demonstration)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

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
![model architecture](https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/model_arch_diagram.png)


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
$ rosrun iq_gnc movement.py              # Start the drone
```

The YouTube link below brings you to a video of the script running:
<p align="center">
  <a href="https://www.youtube.com/watch?v=liCptHpHUXY" target="_blank">
    <img src="https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/thumbnail.PNG" alt="Your Image Alt Text" width=70% height=70%>
  </a>
</p>

aerial_image_processed_0.jpg
<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_0.jpg" alt="Image 1" width="48%">
  <p>Image 1</p>
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_1.jpg" alt="Image 2" width="48%">
  <br>
  <p>Image 2</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_2.jpg" alt="Image 3" width="48%">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_3.jpg" alt="Image 4" width="48%">
  <br>
  <p>Image 3</p>
  <p>Image 4</p>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/shenrunzhang/ROS-Drone-Object-Detection/master/media/aerial_image_processed_4.jpg" alt="Image 5" width="100%">
  <br>
  <p>Image 5</p>
</div>






