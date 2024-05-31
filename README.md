![Sarcomere Dynamics Inc.](/public/SarcomereLogoHorizontal.svg)
# Artus Lite Python API
This repository contains the Python API for controlling the Artus Lite Robotic Hand developed and maintained by Sarcomere Dynamics Inc. Please contact the team if there are any questions or issues that arise through the use of the API. 

The `artus_lite_api` folder is required to be copied into your project for use. 

## Table of Contents
* [Requirements & Install](#requirements--install)
    * [USB Driver](#usb-driver)
* [API Core](#api-core)
    * [Parameters](#parameters)
    * [Class Methods](#class-methods)
* [Joint Class](#joint-class)
    * [Parameters](#parameters-1)
    * [Class Variables](#class-variables)
    * [Class Methods](#class-methods-1)
    * [A note about joint limits](#a-note-about-joint-limits)
* [Running example.py](#running-examplepy)
    * [Control Flow](#control-flow)
    * [Editing the Grasp Files](#editing-grasp-text-files)
* [Implementation Examples](#implementation-examples)
    * [Setting input values](#setting-input-values)
    * [Getting feedback values](#getting-feedback-values)
    * [Controlling multiple hands](#controlling-multiple-hands)
* [Teleoperation Considerations](#teleoperation-considerations)
* [Firmware Updates](#firmware-updates)
* [Revisions](#revisions)

## Requirements & Install
The API is a python based API developed and tested on `Python >= 3.10` please visit the [Python website](https://www.python.org/downloads/) to install Python.

To install the pip libraries, please run the following commands:\
`cd artus_lite_api`\
`pip install -r requirements.txt`

### USB Driver
If the host system cannot find the Artus Lite as a USB device once it is connected over USBC, go to [FTDI Driver Download](https://ftdichip.com/drivers/vcp-drivers/) to install the virtual COM port driver. 

## API Core
```python
class ArtusAPI()
```

### Parameters:
- **communication_method**: UART or WiFi.
- **port**: COM port for UART
- **target_ssid**: default will be set when shipped but replace with whatever your Artus Lite hand WiFi network name is. Only necessary for WiFi

Note that there should only be one single machine running one instance of the API to control 1-2 hands.

### Class Methods:
- **`start_connection`**: start the connection to the Artus Lite over WiFi or UART as specified
- **`start_robot`**: send a start command to the Artus Lite over WiFi or UART as specified
- **`close_connection`**: close the connection to the Artus Lite over WiFi or UART as specified
- **`send_target_command`**: sends a targetting command based on the `input` data fields in the joint dictionary
- **`get_robot_states`**: send a message to the Artus Lite to receive joint data and populates `feedback` data fields in joints
- **`calibrate`**: send a calibrate command to the Artus Lite over WiFi or UART as specified
- **`sleep`**: send a sleep command to the Artus Lite over WiFi or UART as specified that saves the current positions of the hand to non-volatile memory in preparation for power cycling
- **`save_grasp_pattern`**: save a grasp pattern in robot_command to a text file in grasp_patterns folder
- **`get_grasp_pattern`**: get a grasp patptern from a text file in grasp_patterns folder

## Joint Class
```python
class ArtusLiteJoint()
```
### Parameters:
- **`joint_name`**: name of the joint
- **`maximum_angle_constraint` and `minimum_angle_constraint`**: angle constraints
- **`maximum_speed_constraint` and `minimum_speed_constraint`**: speed constraints

### Class Variables:
- **`input_speed`**: input speed for next target
- **`input_angle`**: input angle for next target
- **`feedback_angle`**: reported angle
- **`feedback_temperature`**: reported temperature of actuator associated with the joint
- **`feedback_current`**: reported current of actuator associated with joint

### Class Methods:
- **`check_input_constraints`**: called automatically in `send_target_command`, this ensures that values written to the Artus Lite are in the format expected

![Hand Joint Array Image Map](/public/Hand_Joint_Map.png)

### A note about joint limits:
* All D2, D1 and flex joints have a range of 0-90 degrees
* Thumb spread is between -30 and 30, while the rest of the spreads are -15 to 15. 

## Running example.py
Before running the example script, determine whether your Artus Lite is running WiFi or UART, and edit the following line with the name of the target SSID for WiFi and port over UART

* On Windows, find the port name by navigating to "Device Manager">"Ports". It should show up as a COM port. (e.g. COM3)
* On Linux, use the command `dmesg | grep ttyUSB` to find the usb device. (e.g. /dev/ttyUSB1)
    * If a permission error is encountered, use the command `sudo chmod 777 /dev/ttyUSB1` 

```python
artus_lite = ArtusAPI(target_ssid='Artus3DLH',port='/dev/ttyUSB0',communication_method='Wifi')
```
When running the example script, the following menu will be shown within the terminal:
```
Artus Lite API v1.1.0
Command options:
1. start connection to hand
2. start robot
3. calibrate
4. send command from grasp_patterns/example_command.txt
5. get states
6. open hand from grasp_patterns/grasp_open.txt
7. close hand using grasp in grasp_patterns/grasp.txt
8. save current hand state for power cycle
9. close connection


r : reset joint
Fun Hand Signs:
s : Spock
p : Peace
d : Devil Ears
o : Number One
l : pinch
Enter command: 
```
### Control Flow
The first thing to do is to start the connection to the hand by pressing "1". 

Next, you want to send the start robot command "2". 

Next to send a command, you can edit the `example_command.txt` file in the grasp_patterns folder. 

### Editing Grasp text files
*Note when editing the grasps files:*\
`c176p[+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00]v[+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90]end`

The first array[] of 16 elements is the input angle in degrees mapped to the joints as shown in the hand joint map, and the second array[] of 16 elements is the input speed in percentage mapped to the joints as shown in the hand joint map.

e.g. to set the `thumb_flex` to 45 degrees which is associated with index 0, you would change the first element in the first array so that the new command would be:\
`c176p[+45,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00,+00]v[+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90,+90]end`

To edit the command there are a few things that need to be accounted for:
* each element in the array has 3 characters and must follow this convention
    * examples of allowable angles `+06` or `+90` or `-10` as these are all 3 characters long
    * velocities are in percentage, and should range from `+75` to `100` - note `100` does not have a +/- in front of it as it is already 3 characters in length
    * if this command convention is not followed, the hand may act unpredictably

## Implementation Examples
Below are some examples of how you can implement these functions in your code that are not covered by the `example.py` script.\
### Setting input values:
*Name accessible :*
```python
artus_lite.joints['thumb_flex'].input_angle = 45
```
*Through a Loop :*\
In this example, the assumption is you have an array of angles that are already mapped to the indices of the Artus Lite
```python
# input angles come from your control code, have 16 elements of type int or float and are mapped to our hand joint map
input_angles_from_control = []

for joint,joint_info in artus_lite.joints.items():
    joint_info.input_angle = input_angles_from_control[joint_info.index]
```

### Getting feedback values:
In the same way as setting input values, we can access feedback data after calling `artus_lite.get_robot_states()` by name.\
*Name accessible :*
```python
artus_lite.joints['thumb_flex'].feedback_angle
```

### Controlling multiple hands:
We can define two instances of hands with different `port` and `target_ssid`. In theory, it can spin up an unlimited amount of hands, bottlenecked by the amount of wifi controllers and COM ports associated with the machine. e.g.
```python
artus_liteLeft = Artus3DAPI(target_ssid='Artus3DLH',port='/dev/ttyUSB0',communication_method='UART')
artus_liteRight = Artus3DAPI(target_ssid='Artus3DRH',port='/dev/ttyUSB1',communication_method='UART')
artusHands = [artus_liteLeft,artus_liteRight]
``` 

## Teleoperation Considerations
** **IT IS IMPORTANT TO ADD A DELAY BETWEEN SENDING MESSAGES, CURRENT SUGGESTED FREQUENCY FOR BEST USE IS 10 Hz OR DELAY OF 0.1s** **

## Directory Structure
```bash
artus_lite_api
├── ArtusAPI.py # Python API for Artus Lite
├── src # Dependencies for the API
│   ├── python_server.py # for WiFi communication
│   ├── python_uart.py # for UART communication
|   └── Artus3DJoint.py # our Joint class
├── requirements.txt # for easy pip install
grasp_patterns
├── grasp_patterns # grasps folder
examples
├── example.py # for easy pip install
public
README.md
```

## Revision Control
| Date  | Revision | Description | 
| :---: | :------: | :---------: |
| Nov. 14, 2023 | v1.0 | Initial release - Artus Lite Mk 5 |
| Apr. 23, 2024 | v1.1 | Beta release - Artus Lite Mk 6 |