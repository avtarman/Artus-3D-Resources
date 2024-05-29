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
rh: reset all joints

Fun Hand Signs:
s : Spock
p : Peace
d : Devil Ears
o : Number One
t : Trial (debugging purposes)
Enter command: ''')

def json_to_command(filename:str,artusapi:ArtusAPI):
    with open(os.path.join('grasp_patterns',filename),'r') as file:
        grasp_dict = json.load(file)
        for name,values in grasp_dict.items():
            artusapi.set_robot_params_by_joint_name(name,values['input_angle'],values['input_speed'])
        artusapi.send_target_command()

def reset_low_all(artusapi:ArtusAPI):
    artusapi.locked_reset_low('0','0')
    time.sleep(1)
    artusapi.locked_reset_low('2','0')
    time.sleep(1)
    artusapi.locked_reset_low('4','0')
    time.sleep(1)
    artusapi.locked_reset_low('6','0')
    time.sleep(1)
    artusapi.locked_reset_low('7','0')
    time.sleep(1)
    artusapi.locked_reset_low('10','0')
    time.sleep(1)
    artusapi.locked_reset_low('12','0')
    time.sleep(1)
    artusapi.locked_reset_low('13','0')
    time.sleep(1)

def read_feedback(artus3d: ArtusAPI, frequency = 2):
    last_read_time = time.perf_counter()
    while True:
        try:
            if time.perf_counter() - last_read_time > 1 / frequency:
                joints = artus3d.get_robot_states()
                # joint_positions_only = []
                # for name, joint in joints.items():
                #     joint_positions_only.append(joint.feedback_angle)
                # print(f'Feedback for zmq: {joint_positions_only}')

                last_read_time = time.perf_counter()
        except KeyboardInterrupt:
            break




def example():
    artus3d = ArtusAPI(port='COM3',communication_method=UART,hand='left')
    # artus3d = ArtusAPI(target_ssid='ArtusMK6RH',port='/dev/ttyUSB0',communication_method=UART,hand='right')
    while True:
        try:
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
                    read_feedback(artus3d, frequency=2)
                case "7":
                    artus3d.sleep()
                case "8":
                    artus3d.close_connection()    

                case "r":
                    j = input('enter joint index to reset')
                    m = input('enter motor 0 - both | 1 - m1 | 2 - m2')
                    artus3d.locked_reset_low(j,m)

                case "rh":
                    reset_low_all(artus3d)
                case "s":
                    json_to_command('spock.json',artus3d)
                case "p":
                    json_to_command('peace.json',artus3d)
                case "d":
                    json_to_command('devil_ears.json',artus3d)
                case "o":
                    json_to_command('one.json',artus3d)
                case "t":
                    json_to_command('trial.json', artus3d)
                    read_feedback(artus3d, frequency=2)
                case "x":
                    json_to_command('pre_grab_disk.json', artus3d)
                    read_feedback(artus3d, frequency=2)
                case "y":
                    json_to_command('grab_disk.json', artus3d)
                    read_feedback(artus3d, frequency=2)
        except KeyboardInterrupt:
            print('')

if __name__ == '__main__':
    example()


