import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI,UART,WIFI


artus3d = Artus3DAPI(target_ssid='ArtusMK6RH',port='COM7',communication_method=UART,hand='right')
artus3d.start_connection()

x = input('go')

while True:
    x = input('close') # grab drill
    with open(os.path.join("grasp_patterns","example_command.txt"), "r") as f:
        command = f.read()
    if command != "":
        artus3d.send_target_command(command)

    # time.sleep(3)

    x = input('open') # trigger
    with open(os.path.join("grasp_patterns","spock.txt"), "r") as f:
        command = f.read()
    if command != "":
        artus3d.send_target_command(command)

    # time.sleep(3)