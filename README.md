<img src='data/images/SarcomereLogoHorizontal.svg'>

# Python Artus Robotic Hand API

This repository contains a Python API for controlling the Artus robotic hands by Sarcomere Dynamics Inc.

Please contact the team if there are any issues that arise through the use of the API.

## Introduction

>[!IMPORTANT]
__Please read through the entire README before using the Artus hand__

Below are some critical information while using the Artus hand.

### Note about Calibration & Power Cycling

Below are some some notes about some key fields that are required in different situations to reduce the number of calibration sequences needed to run.

* When powering off the hand, or closing the control script, the hand needs to be in an __OPEN__ state to reduce amount of calibration and jamming. If the hand is closed when powered off, the `__reset_on_start__` parameter needs to be set to `1` to open the hand before starting

* Using the `__awake__` parameter: if the hand is already in a ready state (LED is green) when starting or restarting a control script, set awake to `True` to bypass resending the `wake_up` function, which could lead to lost calibration.

* Ready State: The Artus Lite has an indicator LED that indicates the state of the hand. If the hand is __BLUE__, the hand is __NOT READY FOR TARGET, CALIBRATE COMMANDS__. The hand is only ready for these commands when the LED is __GREEN__. 


* Artus Lite specific technical details are available within the [robot folder](/ArtusAPI/robot/artus_lite/)

## Table of Contents
- [Python Artus Robotic Hand API](#python-artus-robotic-hand-api)
  - [Introduction](#introduction)
    - [Note about Calibration \& Power Cycling](#note-about-calibration--power-cycling)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Video Introduction](#video-introduction)
    - [Requirements](#requirements)
      - [USB Driver](#usb-driver)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Running example.py](#running-examplepy)
    - [Creating an ArtusAPI Class Object](#creating-an-artusapi-class-object)
      - [Serial Example](#serial-example)
    - [Normal Startup Procedure](#normal-startup-procedure)
  - [DIO](#dio)
  - [Setting Grasps - SD Card](#setting-grasps---sd-card)
  - [Interacting with the API](#interacting-with-the-api)
    - [Setting Joints](#setting-joints)
    - [Input Units](#input-units)
    - [Getting Feedback](#getting-feedback)
    - [Controlling multiple hands](#controlling-multiple-hands)
  - [Teleoperation Considerations](#teleoperation-considerations)
  - [Directory Structure](#directory-structure)
  - [Artus Lite Control Examples Setup](#artus-lite-control-examples-setup)
    - [1. GUI Setup](#1-gui-setup)
    - [2. ROS2 Node Control Setup](#2-ros2-node-control-setup)
    - [3. Manus Glove Setup](#3-manus-glove-setup)
  - [Revision Control](#revision-control)

## Getting Started
### Video Introduction
[![Getting Started Video](/data/images/thumbnail.png)](https://www.youtube.com/watch?v=30BkuA0EkP4)

### Requirements
Requires Python version >= 3.10 installed on the host system. Please visit the [Python website](https://www.python.org/downloads/) to install Python.

#### USB Driver
>[!NOTE]
If the host system cannot find the Artus Lite as a USB device once it is connected over USBC, go to [FTDI Driver Download](https://ftdichip.com/drivers/vcp-drivers/) to install the virtual COM port driver (usually only required for Windows). 

### Installation
Using pip:
```bash
pip install psutil
pip install pyserial
pip install ArtusAPI
```

__Alternatively, cloning the repository and using the repository locally in a project scope is another option, it may be more up-to-date than the pip stable release.__

## Usage

### Running example.py
Before running the example script, determine whether your Artus Lite is running USB Serial or WiFi, and edit the following line with the name of the port over UART or target SSID for WiFi

* On Windows, find the port name by navigating to "Device Manager">"Ports". It should show up as a COM port. (e.g. COM3)
* On Linux, use the command `dmesg | grep ttyUSB` to find the usb device. (e.g. /dev/ttyUSB1)
    * If a permission error is encountered, use the command `sudo chmod 777 /dev/ttyUSB1` 

Linux: 
```python
artusapi = ArtusAPI(communication_method='UART',hand_type='right',communication_channel_identifier='/dev/ttyUSB1',reset_on_start=0)
```

Windows:
```python
artusapi = ArtusAPI(communication_method='UART',hand_type='right',communication_channel_identifier='COM3')
```

### Creating an ArtusAPI Class Object
Below are some examples of instantiating the ArtusAPI class to control a single hand. Below is a description of the parameters and what they mean.

* `__communication_method__` : The communication method between the host system and the Artus hand
* `__communication_channel_identifier__` : The identifying parameter of the communication method such as COM port over Serial or network name over WiFi
* `__robot_type__` : The Artus robot hand name 
* `__hand_type__` : left or right hand
* `__stream__` : whether streaming feedback data is required or not. Default: `False`
* `__communication_frequency__` : The frequency of the feedback and command communication. Default: `200` Hz
* `__logger__` : If integrating the API into control code, you may already have a logger. THis will allow for homogeneous logging to the same files as what you currently have. Default: `None`
* `__reset_on_start__` : If the hand is not in a closed state when last powered off, setting to `1` will open the hand before ready to receive commands. This _MUST_ be set if powered off in a closed state, and a calibrate may need to be run before sending accurate target commands
* `__baudrate__` : required to differentiate between Serial over USB-C and Serial over RS485, default `921600`
* `__awake__` : False by default - if the hand is already in a ready state (LED is green) when starting or restarting a control script, set woken to `True` to bypass resending the `wake_up` function, which could lead to lost calibration.

#### Serial Example
```python
from ArtusAPI.artus_api import ArtusAPI
artus_lite = ArtusAPI(robot_type='artus_lite', communication_type='UART',hand_type='right',communication_channel_identifier='COM7',reset_on_start=0)

artus_lite.connect()
```

### Normal Startup Procedure
There is a standard series of commands that need to be followed before sending target commands or receiving feedback data is possible. 

Before any software, ensure that the power connector is secured and connected to the Artus hand and if using a wired connection (Serial or CANbus), ensure the connection/cable is good. 

First, to create a communication connection between the API and the Artus hand, `ArtusAPI.connect()` must be run to confirm communication is open on the selected communication type.

Second, the `ArtusAPI.wake_up()` function must be run to allow the hand to load it's necessary configurations.

Once these two steps are complete, optionally, you can run `ArtusAPI.calibrate()` to calibrate the finger joints. Otherwise, the system is now ready to start sending and receiving data!

>[!NOTE]
>If running version v1.0.1, `wake_up` is called inside the `connect()` function_

## DIO
| DIO | Wire Colour | Function |
| --- | --- | --- |
| DI0 | Yellow | Grasp 1 from SD Card |
| DI1 | Green | Grasp 2 from SD Card |
| DO0 | Blue | Status - HIGH = Ready, LOW = Not Ready/Error |
| DO1 | Pink | Status - HIGH = Idle/in Motion, LOW = Target Achieved |

## Setting Grasps - SD Card
Before using the Artus Lite's digital IO functionality to communicate with a robotic arm, there are two steps that need to be done. 
1. Users must set the grasps that they want to call. This is done through the UI, using the `save_grasp_onhand` command. This command will save the last command sent to the hand in the designated position specified (1-6) on the SD card and persist through resets.
2. Users can use the `execute_grasp` command to call the grasps through the API. 

Each of the above will print the command to the terminal.

## Interacting with the API
To get the most out of the Artus hands, the functions that will likely be most interacted with are `set_joint_angles(self, joint_angles:dict)` and `get_joint_angles(self)`. The `set_joint_angles` function allows the user to set 16 independent joint values with a desired velocity/force value in the form of a dictionary. See the [grasp_close file](data/hand_poses/grasp_close.json) for an example of a full 16 joint dictionary for the Artus Lite. See the [Artus Lite README](ArtusAPI/robot/artus_lite/README.md) for joint mapping.

e.g. 
```python
artusapi.set_joint_angles(pinky_dict)
```

### Setting Joints
As mentioned above, there are 16 independent degrees of freedom for the Artus Lite, which can be set simultaneously or independently. If, for example, a user need only curl the pinky, a shorter dictionary like the following could be used as a parameter to the function:

```
pinky_dict = {"pinky_flex" : 
                            {
                                "index": 14,
                                "input_angle" : 90
                            },
              "pinky_d2" :
                            {
                                "index":15,
                                "input_angle" : 90
                            }
            }

ArtusAPI.set_joint_angles(pinky_dict)
```

Notice that the above example does not include the `"input_speed"` field that the json file has. The `"input_speed"` field is optional and will default to the nominal speed.

### Input Units
* Input Angle: the input angle is an integer value in degrees
* velocity: the velocity is in a percentage unit 0-100. Minimum movement requirement is around 30. This value pertains to the gripping force of the movement. 

### Getting Feedback
There are two ways to get feedback data depending on how the class is instantiated.

1. In streaming mode (`stream = True`), after sending the `wake_up()` command, the system will start streaming feedback data which will populate the `ArtusAPI._robot_handler.robot.hand_joints` dictionary. Fields that hold feedback data are named with `feedback_X` where _X_ could be angle, current or temperature.
2. In Request mode (`stream = False`), sending a `get_joint_angles()` command will request the feedback data before anything is sent from the Artus hand. This communication setting is slower than the streaming mode, but for testing purposes and getting familiar with the Artus hand, we recommend starting with this setting. 

### Controlling multiple hands
We can define two instances of hands with different `port` and `target_ssid`. In theory, it can spin up an unlimited amount of hands, bottlenecked by the amount of wifi controllers and COM ports associated with the machine. e.g.
```python
artus_liteLeft = Artus3DAPI(target_ssid='Artus3DLH',port='/dev/ttyUSB0',communication_method='UART')
artus_liteRight = Artus3DAPI(target_ssid='Artus3DRH',port='/dev/ttyUSB1',communication_method='UART')
artusHands = [artus_liteLeft,artus_liteRight]
``` 

## Teleoperation Considerations
For teleoperation, there is a parameter for the class that lets the user set the `communication frequency` without adding delays into the communication.

```python
artus_liteLeft = Artus3DAPI(target_ssid='Artus3DLH',port='COM5',communication_method='UART',communication_frequency = 100)
``` 

## Directory Structure
```bash
├── ArtusAPI
│   ├── commnands
│   │   ├── commands.py # Command strings for the Robot Hand
│   ├── communication
│   │   ├── WiFi
│   │   │   ├── WiFi.py # WiFi communication class
│   │   ├── UART
│   │   │   ├── UART.py # UART communication class
│   │   ├── communication.py # Communication class for the API
│   ├── robot
│   │   ├── artus_lite
│   │   │   ├── artus_lite.py # Artus Lite Hand class
│   │   ├── robot.py # Robot Hand class for the API
│   ├── artus_api.py # API Core
```

## Artus Lite Control Examples Setup

### 1. GUI Setup
Please check the [Artus GUI](https://github.com/Sarcomere-Dynamics/Sarcomere_Dynamics_Resources/tree/main/examples/Control/ArtusLiteControl/GUIControl) for a GUI setup to control the Artus Lite hand.

Also, check the video below for a demonstration of the GUI setup.

<div align="center">
  <a href="https://www.youtube.com/watch?v=l_Sl6bAeGuc">
    <img src="./data/images/gui.png" alt="Watch the video" width="200" />
  </a>
</div>

### 2. ROS2 Node Control Setup
Please check the [Artus ROS2 Node](https://github.com/Sarcomere-Dynamics/Sarcomere_Dynamics_Resources/tree/main/ros2/artuslite_ws) for a ROS2 node setup to control the Artus Lite hand.

Also, check the video below for a demonstration of the ROS2 node setup.

<div align="center">
  <a href="https://www.youtube.com/watch?v=GHyG1NuuRv4">
    <img src="./data/images/ros2_logo.jpg" alt="Watch the video" width="200" />
  </a>
</div>


### 3. Manus Glove Setup

Please check the [Manus Glove](https://github.com/Sarcomere-Dynamics/Sarcomere_Dynamics_Resources/tree/main/examples/Control/ArtusLiteControl/ManusGloveControl) for a Manus Glove setup to control the Artus Lite hand.

Also, check the video below for a demonstration of the Manus Glove setup.

<div align="center">
  <a href="https://www.youtube.com/watch?v=SPXJlxMaDVQ&list=PLNUrV_GAAyA8HNBAvwBlsmIqoWiJJLRwW&index=2">
    <img src="./data/images/manus.jpg" alt="Watch the video" width="200" />
  </a>
</div>


## Revision Control
| Date  | Revision | Description | Pip Release |
| :---: | :------: | :---------: | :----------: |
| Nov. 14, 2023 | v1.0b | Initial release - Artus Lite Mk 5 | NA |
| Apr. 23, 2024 | v1.1b | Beta release - Artus Lite Mk 6 | NA |
| Oct. 9, 2024 | v1.0 | Artus Lite Release | v1.0 |
| Oct. 23, 2024 | v1.0.2 | awake parameter added, wake up function in connect | v1.0.1 |
