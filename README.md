# ROS Drone Object Detection
An implementation of a vision pipeline for target detection and classification, incorporating a custom-trained CNN model and Holistically-Nested Edge Detection (HED) deep learning model. A working demonstration is shown with ROS and Gazebo.

## Table of Contents

- [About](#about)
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

## Demonstration






<p align="center">
  <a href="https://www.youtube.com/watch?v=liCptHpHUXY" target="_blank">
    <img src="https://github.com/shenrunzhang/ROS-Drone-Object-Detection/blob/master/media/thumbnail.PNG" alt="Your Image Alt Text" width=70% height=70%>
  </a>
</p>
