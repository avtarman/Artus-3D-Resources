
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
    hand_robot_api.joint_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ## 2.2 Set Joint Velocities
    hand_robot_api.joint_velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ## 2.3 Set Joint Accelerations
    hand_robot_api.joint_acceleration = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ## 2.4 Send Command to Robot
    hand_robot_api.send_command()
    # 3. Get Robot States
    robot_states = hand_robot_api.get_robot_states()



def application_demo():

    hand_robot_api = Artus3DAPI()

    USER_INTERFACE = "Select one of the following options:\n" \
                        "1. Calibrate Robot\n" \
                        "2. To change communication method\n" \
                        "3. To send command to robot\n" \
                        "4. Save grasp patterns\n" \
                        "5. Get robot states\n" \
                        "6. Use grasp pattern\n" \
                        
    while True:
        user_input = input(USER_INTERFACE)
        if user_input == "1":
            hand_robot_api.calibrate()
            time.sleep(1)
            hand_robot_api.receive()
        elif user_input == "2":
            communication_method = input("Enter communication method: ")
            hand_robot_api.change_communication_method(communication_method)
            time.sleep(1)
            hand_robot_api.receive()
        elif user_input == "3":
            command_to_send = input("Enter command to send: ")
            hand_robot_api.send(command_to_send)
            time.sleep(1)
            hand_robot_api.receive()
        elif user_input == "4":
            hand_robot_api.save_grasp_pattern()
        elif user_input == "5":
            command = "c16p[30,00,00,00,30,00,00,30,00,00,30,00,00,30,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]a[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
            hand_robot_api.send(command)
            robot_states = hand_robot_api.get_robot_states()
      
            print(robot_states)

        elif user_input == "6":
            grasp_pattern = hand_robot_api.load_grasp_patterns()
            grasp_name_to_use = input("Enter grasp name to use: ")
            if grasp_name_to_use in grasp_pattern:
                hand_robot_api.send(str(grasp_pattern[grasp_name_to_use]))
                print(grasp_pattern[grasp_name_to_use])
            else:
                print("Grasp name not found.")
        else:
            print("Invalid input. Try again.")





if __name__ == '__main__':
    application_demo()
