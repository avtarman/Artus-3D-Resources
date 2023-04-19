
import time

import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from artus_3d_api import Artus3DAPI

def main():
    # create a hand_robot_api object
    hand_robot_api = Artus3DAPI()

    # 1. Set Commands
    # 1.1 Set Joint Angles
    hand_robot_api.joint_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # # 1.2 Set Joint Velocities
    hand_robot_api.joint_velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # # 1.3 Set Joint Accelerations
    hand_robot_api.joint_acceleration = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # # 1.4 Send Command to Robot
    hand_robot_api.send_command()

    # 2. Get Robot States
    robot_states = hand_robot_api.get_robot_states()
    print(robot_states)

    # 3. Teleoperation Mode
    teleoperation_mode = False # make it True if teleoperation control

    if teleoperation_mode:
        i = 0
        while True:
            
            hand_robot_api.joint_angles[0] = i
            hand_robot_api.teleoperation_mode(joint_angles= hand_robot_api.joint_angles)
            time.sleep(0.02)
            i += 1

if __name__ == '__main__':
    main()
