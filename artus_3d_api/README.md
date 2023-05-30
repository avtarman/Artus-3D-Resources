# Artus 3D API

API for controlling the Artus 3D dexterous robotic hand.

# Directory Structure
```bash
├── artus_3d_api.py # Python API for Artus 3D
├── example.py # Example usage of the API
├── src # Dependencies for the API
│   ├── python_server.py # for WiFi communication
│   └── python_uart.py # for UART communication
```


# API Core

## Artus3DAPI


```python
class Artus3DAPI(communication_method: str = 'WiFi')
```
Provides an API for controlling the Artus 3D dexterous robotic hand.

**Parameters**:
- **communication_method**: Communication method to use. Can be either 'WiFi' or 'UART'. Defaults to 'WiFi'.

**Methods**:
- **calibrate()**: send calibration command to the hand.
- **shutdown()**: send shutdown command to the hand.
- **set_joint_angles(joint_angles: List[float])**: Sets the joint angles to be sent to the hand.
- **set_joint_velocities(joint_velocities: List[float])**: Sets the joint velocities to be sent to the hand.
- **set_joint_accelerations(joint_accelerations: List[float])**: Sets the joint accelerations to be sent to the hand.
- **send_command()**: Sends the command to the hand.
- **get_robot_states()**: Gets the robot states from the hand.
- **save_grasp_pattern(command_name: str)**: Saves the current joint configuration as a grasp pattern.
- **load_grasp_patterns()**: Loads the grasp patterns as a dictionary.

## Procedure

1. Power on the hand.
2. Connect to the ESP32 WiFi network on your computer.
3. Run the API.


## Usage

- Import the API
```python
from artus_3d_api import Artus3DAPI
```

- Create an instance of the API
```python

# for WiFi communication
api = Artus3DAPI()  # defaults to WiFi communication

# for UART communication
api = Artus3DAPI(communication_method='UART')
```

- Calibrate the hand
```python
api.calibrate()
```

- Set the joint angles
```python
api.set_joint_angles([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
```

- Send the command to the hand
```python
api.send_command()
```

- Get the robot states from the hand
```python
api.get_robot_states()
```

- Get Debug Info from the hand
```python
api.get_debug_messages()
```

- Shutdown the hand
```python
api.shutdown()
```

- Save the current joint configuration as a grasp pattern
```python
api.save_grasp_pattern('open') # 'open' is the name of the grasp pattern
```

- Load the grasp patterns as a dictionary
```python
grab_patterns = api.load_grasp_patterns() # grab_patterns is a dictionary
```


# Example

```python
from artus_3d_api import Artus3DAPI

api = Artus3DAPI()

api.calibrate()

api.set_joint_angles([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

api.send_command()

states = api.get_robot_states()

debug_messages = api.get_debug_messages()

api.shutdown()

api.save_grasp_pattern('open')

grab_patterns = api.load_grasp_patterns()
```




