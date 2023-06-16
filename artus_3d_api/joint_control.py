

import time

import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from artus_3d_api import Artus3DAPI

def main():
    # create a hand_robot_api object
    hand_robot_api = Artus3DAPI()

 



    # 1. Callibrate Robot
    hand_robot_api.calibrate()
    # 2. Set Commands
    ## 2.1 Set Joint Angles
    hand_robot_api.joint_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # position control
    ## 2.2 Set Joint Velocities
    hand_robot_api.joint_velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 0 for constant velocity control
    ## 2.3 Set Joint Accelerations
    hand_robot_api.joint_acceleration = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # 0 for no effort control
    ## 2.4 Send Command to Robot
    hand_robot_api.send_command() # send command to robot
    # 3. Get Robot States
    robot_states = hand_robot_api.get_robot_states()



def application_demo():

    # hand_robot_api = Artus3DAPI()
    # serial communication
    hand_robot_api = Artus3DAPI() #communication_method = "UART"
    time.sleep(5)

    # User Interface, 1 for callibrate, 2 for start, 3 for target

    while True:

        user_input = input("Select one of the following options:\n" \
                            "1. Calibrate Robot\n" \
                            "2. Start\n" \
                            "3. Target\n" \
                            "4. Exit\n" \
                            "Enter your choice: ")
        if user_input == "1":
            # calibrate robot
            hand_robot_api.calibrate()
            time.sleep(5)
            # hand_robot_api.receive()

        elif user_input == "2":
            # start
            hand_robot_api.start()
            # hand_robot_api.receive()
            time.sleep(5)

        elif user_input == "3":
            while True:
                with open("joint_angles.txt", "r") as f:
                    command = f.read()
            #     # send command to robot
                hand_robot_api.send(command)
                # print(hand_robot_api.receive())
            

            #     # wait for 1 second
                time.sleep(0.2)

        


if __name__ == '__main__':
    application_demo()
