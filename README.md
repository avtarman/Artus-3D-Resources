![Sarcomere Dynamics Inc.](/public/SD_logo.png)
# ArtusAPI ROS2 Humble
This repository contains the Python API for controlling the Artus 3D Robotic Hand developed and maintained by Sarcomere Dynamics Inc. Please contact the team if there are any questions or issues that arise through the use of the API. 

## Table of Contents
* [Requirements](#requirements--install)
* [API Core](#api-core)
    * [Parameters](#parameters)
    * [Class Methods](#class-methods)
* [Joint Class](#joint-class)
    * [Parameters](#parameters-1)
    * [Class Variables](#class-variables)
    * [Class Methods](#class-methods-1)
    * [A note about joint limits](#a-note-about-joint-limits)
* [Running example.py](#running-examplepy)
* [Implementation Examples](#implementation-examples)
    * [Setting input values](#setting-input-values)
    * [Getting feedback values](#getting-feedback-values)
    * [Controlling multiple hands](#controlling-multiple-hands)
* [Teleoperation Considerations](#teleoperation-considerations)
* [Firmware Updates](#firmware-updates)
* [Revisions](#revisions)

## Requirements & Install
- Ubuntu 22.04
- ROS2 Humble
- Python 3
- Colcon

## Getting Started
1. Clone the code using
git clone <this repo>

2. Install required libraries

cd path/to/project
 3. Build ROS2 package
 ...

 4. Change Parameters in the Launch File

 5. Run the Launch file
