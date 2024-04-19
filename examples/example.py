import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
# print(os.path.dirname(current_directory))
from artus_3d_api.Artus3DAPI import Artus3DAPI,UART,WIFI

def main_menu():
    return input('''
Artus 3D API v1.0.0
Command options:
1. start connection to hand
2. start robot
3. calibrate
4. send command from grasp_patterns/example_command.txt
5. get states
6. open hand from grasp_patterns/grasp_open.txt
7. close hand using grasp in grasp_patterns/grasp.txt
8. save current hand state for power cycle
9. close connection
                 
Fun Hand Signs:
s : Spock
p : Peace
d : Devil Ears
o : Number One
l : pinch
Enter command: ''')

LHB = 'Artus3DTesterLHBLACK'
LHW = 'Artus3DTesterLHWHITE'
LHW = 'Artus3DTesterLHWHITE'
RHW = 'Artus3DTesterRHWHITE'
MK6LH = 'ArtusMK6LH'
MK5LH = 'ArtusMk5LH'
RW = 'Artus3DRW'

def example():
    # artus3d = Artus3DAPI(port='COM11',communication_method=UART,hand='left')
    artus3d = Artus3DAPI(target_ssid='ArtusMK6RH',port='/dev/ttyUSB0',communication_method=UART,hand='right')
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
                with open(os.path.join("grasp_patterns","example_command.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "5":
                artus3d.get_robot_states()
            case "6":
                with open(os.path.join("grasp_patterns","grasp_open.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "7":
                with open(os.path.join("grasp_patterns","grasp.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "8":
                artus3d.sleep()
            case "9":
                artus3d.close_connection()    

            case "r":
                j = input('enter joint index to reset')
                m = input('enter motor 0 - both | 1 - m1 | 2 - m2')
                artus3d.locked_reset_low(j,m)
            case "s":
                with open(os.path.join("grasp_patterns","spock.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "p":
                with open(os.path.join("grasp_patterns","peace.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "d":
                with open(os.path.join("grasp_patterns","devil_ears.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "o":
                with open(os.path.join("grasp_patterns","one.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)
            case "l":
                with open(os.path.join("grasp_patterns","pinch.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send_target_command(command)

if __name__ == '__main__':
    example()


