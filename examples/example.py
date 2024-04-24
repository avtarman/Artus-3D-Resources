import time
import json
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
# print(os.path.dirname(current_directory))
from artus_lite_api.ArtusAPI import ArtusAPI,UART,WIFI

def main_menu():
    return input('''
Artus Lite API v1.1.0
Command options:
1. start connection to hand
2. start robot
3. calibrate
4. send command from grasp_patterns/example_command.txt
5. get states
6. open hand from grasp_patterns/grasp_open.txt
7. save current hand state for power cycle
8. close connection

r : reset joint

Fun Hand Signs:
s : Spock
p : Peace
d : Devil Ears
o : Number One
Enter command: ''')

def json_to_command(filename:str,artusapi:ArtusAPI):
    with open(os.path.join('grasp_patterns',filename),'r') as file:
        grasp_dict = json.load(file)
        for name,values in grasp_dict.items():
            artusapi.set_robot_params_by_joint_name(name,values['input_angle'],values['input_speed'])
        artusapi.send_target_command()

def example():
    # artus3d = ArtusAPI(port='COM11',communication_method=UART,hand='left')
    artus3d = ArtusAPI(target_ssid='ArtusMK6RH',port='/dev/ttyUSB0',communication_method=UART,hand='right')
    while True:
        user_input = main_menu()
        match user_input:
            case "1":
                artus3d.start_connection()
            case "2":
                artus3d.start_robot()
            case "3":
                artus3d.calibrate()
            case "4":
                json_to_command('example_command.json',artus3d)
            case "5":
                artus3d.get_robot_states()
            case "6":
                json_to_command('grasp_open.json',artus3d)
            case "7":
                artus3d.sleep()
            case "8":
                artus3d.close_connection()    

            case "r":
                j = input('enter joint index to reset')
                m = input('enter motor 0 - both | 1 - m1 | 2 - m2')
                artus3d.locked_reset_low(j,m)
            case "s":
                json_to_command('spock.json',artus3d)
            case "p":
                json_to_command('peace.json',artus3d)
            case "d":
                json_to_command('devil_ears.json',artus3d)
            case "o":
                json_to_command('one.json',artus3d)

if __name__ == '__main__':
    example()


