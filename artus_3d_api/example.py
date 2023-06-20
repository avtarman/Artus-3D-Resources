
import time

import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from artus_3d_api import Artus3DAPI


def user_input_function():

    print("Enter command to send:\n"
        "1. start\n"
        "2. calibrate\n"
        "3. send command\n"
        "4. save grasp pattern\n"
        "5. use saved grasps")

    return input("Enter command to send: ")


def example():


    hand_robot_api = Artus3DAPI()

    time.sleep(2)

    while True:
        user_input = user_input_function()
        if user_input == "1":
            hand_robot_api.start()
        elif user_input == "2":
            hand_robot_api.calibrate()
        elif user_input == "3":
            with open("C:/Users/bajwa/Desktop/Robot_API/joint_angles.txt", "r") as f:
                command = f.read()
        #     # send command to robot   
            if command != "":
                hand_robot_api.send(command)
        elif user_input == "4":
            hand_robot_api.save_grasp_pattern(grasp_pattern= command)
        elif user_input == "5":
            grasp_pattern = hand_robot_api.get_grasp_command()
            print(grasp_pattern)
            hand_robot_api.send(grasp_pattern)

    #     # wait for 1 second
        time.sleep(1)

if __name__ == '__main__':
    # main()
    example()
