
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
        "5. use saved grasps\n"
        "6. to get robot states\n"
        "7. to get debug messages")

    return input("Enter command to send: ")


def example():

    hand_robot_api = Artus3DAPI()
    # hand_robot_api = Artus3DAPI(communication_method="UART", port="COM8") # change port

    time.sleep(2)

    while True:
        # for i in range(100):
        #     debug_message = hand_robot_api.get_debug_message()
        #     print(debug_message)
        # for i in range(100):
        #     debug_message = hand_robot_api.get_robot_states()
        #     print(debug_message)
        # continue
        user_input = user_input_function()
        if user_input == "1":
            hand_robot_api.start()
        elif user_input == "2":
            hand_robot_api.calibrate()
        elif user_input == "3":
            with open("joint_control_command.txt", "r") as f:
                command = f.read()
        #     # send command to robot   
            if command != "":
                hand_robot_api.send(command)
        elif user_input == "4":
            hand_robot_api.save_grasp_pattern(grasp_pattern= command)
        elif user_input == "5":
            grasp_pattern = hand_robot_api.get_grasp_command()
            #print(grasp_pattern)
            hand_robot_api.send(grasp_pattern)
        elif user_input == "6":
            robot_states  = hand_robot_api.get_robot_states()
            print(robot_states)

        elif user_input == "7":
            debug_message = hand_robot_api.get_debug_message()
            print(debug_message)

    #     # wait for 1 second
        time.sleep(1)


if __name__ == '__main__':
    # main()
    example()
