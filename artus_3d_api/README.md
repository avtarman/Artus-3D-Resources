# Artus 3D API

API for controlling the Artus 3D dexterous robotic hand.

# Directory Structure
```bash
├── artus_3d_api.py # Python API for Artus 3D
├── example.py # Example usage of the API
├── src # Dependencies for the API
│   ├── python_server.py # Python server for the API
│   └── exp32_commands.py # Commands for the API
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
- **set_command(command: int)**: Sets the command to be sent to the hand.
- **set_joint_angles(joint_angles: List[float])**: Sets the joint angles to be sent to the hand.
- **set_joint_velocities(joint_velocities: List[float])**: Sets the joint velocities to be sent to the hand.
- **set_joint_accelerations(joint_accelerations: List[float])**: Sets the joint accelerations to be sent to the hand.
- **send_command()**: Sends the command to the hand.
- **get_robot_states()**: Gets the robot states from the hand.
- **save_grasp_pattern(command_name: str)**: Saves the current joint configuration as a grasp pattern.
- **load_grasp_patterns()**: Loads the grasp patterns as a dictionary.
