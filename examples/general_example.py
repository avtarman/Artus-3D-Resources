import time
import json
import os
import sys
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent
sys.path.append(str(desired_path))

from ArtusAPI.artus_api import ArtusAPI

def main_menu():
    return input(
'''
Artus API 2.0
Command options:
1. start connection to hand
2. close connection
3. wakeup hand
4. sleep hand
5. calibrate
6. send command from data/grasp_poses/grasp_example
7. get robot states
8. send command from data/grasp_poses/grasp_open
Enter command: 
''')

def example():
    artusapi = ArtusAPI(communication_method='UART',hand_type='right',communication_channel_identifier='COM7',reset_on_start=0)
    # artusapi = ArtusAPI(communication_method='UART',hand_type='right',communication_channel_identifier='/dev/ttyUSB1',baudrate=115200)
    while True:
        user_input = main_menu()

        match user_input:
            case "1":
                artusapi.connect()
            case "2":
                artusapi.disconnect()
            case "3":
                # artusapi._command_handler.reset_on_start = 1
                artusapi.wake_up()
            case "4":
                artusapi.sleep()
            case "5":
                artusapi.calibrate()
            case "6":
                with open(os.path.join(desired_path,'data','hand_poses','grasp_example.json'),'r') as file:
                    grasp_dict = json.load(file)
                    artusapi.set_joint_angles(grasp_dict)
            case "7":
                print(artusapi.get_joint_angles())
            case "8":
                with open(os.path.join(desired_path,'data','hand_poses','grasp_open.json'),'r') as file:
                    grasp_dict = json.load(file)
                    artusapi.set_joint_angles(grasp_dict) 
            case 'f':
                artusapi.update_firmware()  
            case 'r':
                artusapi.reset()
            case 'c':
                artusapi.hard_close()
            case 's':
                num = int(input('what index value should this be stored in? (1-6):'))
                if num == None:
                    artusapi.save_grasp_onhand()
                else:
                    artusapi.save_grasp_onhand(num)
            case 'g':
                artusapi.get_saved_grasps_onhand()
            case 'p':
                artusapi.update_param()
            case 'e':
                data = 0
                while 1:
                    data = int(input('enter grasp index to execute from memory (1-6):'))
                    if data in range(1,7):
                        break

                artusapi.execute_grasp(data)


if __name__ == '__main__':
    example()


