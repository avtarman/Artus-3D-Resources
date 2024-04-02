# ArtusAPI ROS2 Humble
ROS2 node for controlling Artus Robots using Artus API

## Table of Contents
* [Requirements](#requirements)
* [Install python dependencies](#install-python-dependencies)
* [Getting Started](#getting-started)


## Requirements
- Ubuntu 22.04
- ROS2 Humble
- Python 3
- Colcon

## Install python dependencies
```bash
pip install -r requirements.txt
```

## Getting Started
1. Clone the code using
git clone <this repo>

2. Install required libraries

3. Change the parameter values to desired values in the "artus_api_bringup.launch.py"
   

4. cd path/to/project and build ROS2 package

   colcon build

 5. Run the Launch file
    ros2 launch artus_api_bringup artus_api_bringup.launch.py

