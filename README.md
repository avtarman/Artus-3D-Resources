# ArtusAPI ROS2 Humble
This repository contains the Python API for controlling the Artus 3D Robotic Hand developed and maintained by Sarcomere Dynamics Inc. Please contact the team if there are any questions or issues that arise through the use of the API. 
![Sarcomere Dynamics Inc.](/public/SD_logo.png)

## Table of Contents
* [Requirements]
* [Getting Started]

## Requirements & Install
- Ubuntu 22.04
- ROS2 Humble
- Python 3
- Colcon

## Getting Started
1. Clone the code using
git clone <this repo>

2. Install required libraries

3. Chnage the parameter values to desired values in the "artus_api_bringup.launch.py"
   

4. cd path/to/project and build ROS2 package

   colcon build

 5. Run the Launch file
    ros2 launch artus_api_bringup artus_api_bringup.launch.py

