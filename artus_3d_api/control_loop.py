import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from artus_3d_api import Artus3DAPI
import keyboard

# import grasps
graspClose = current_directory+"\\grasp_patterns\\grasp_close.txt"
graspOpen  = current_directory+"\\grasp_patterns\\grasp_open.txt"

# fill dict
grasps = {
    "open":graspOpen,
    "close":graspClose
}

# wait time
# delay for UART
delay = 0.01
# no delay for WIFI


def example_control_loop():
    hand_robot_api = Artus3DAPI('UART','COM5')

    time.sleep(1)

    # create command dict
    command_dict = {key: None for key in grasps}

    # load grasps
    for key in grasps:
        with open(grasps[key],'r') as f:
            command_dict[key] = f.read()
    
    # start the hand
    hand_robot_api.start()

    # test counter
    
    j = 0

    while j < 10:
        start = time.time()
        i = 0
        while i<100:
            time.sleep(delay)
            if i%2 == 1:
                hand_robot_api.send(command_dict['open'])
                time.sleep(delay)
            else:
                hand_robot_api.send(command_dict['close'])
                time.sleep(delay)
            # print("getting states")
            # states_string,states = hand_robot_api.get_robot_states()
            # print(states_string)
            # if states['t'][2] == 26: print("yes") 
            i+=1
        end = time.time()
        elapsed = end-start
        print(f"Test {j} - Time elapsed: {elapsed} s")
        j+=1
example_control_loop()