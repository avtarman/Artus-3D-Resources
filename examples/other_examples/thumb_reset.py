# ------------------------------------------------------------------------------
# ---------------------------- Import Libraries --------------------------------
# ------------------------------------------------------------------------------
import time
import json
# Add the desired path to the system path
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("Project Root", PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)
# import ArtusAPI
from Sarcomere_Dynamics_Resources.ArtusAPI.artus_api import ArtusAPI
comport = input("Please enter the USB Device COM Port: ")

def main(com):
    # Initialize ArtusAPI with specified parameters
    artus = ArtusAPI(
        communication_method='UART',
        communication_channel_identifier=com,
        robot_type='artus_lite',
        hand_type='right',
        reset_on_start=0
    )
    
    # number maps to joint name and joint index and motor`
    joint_lut_right_hand = {
        "1" : [0,0],
        "2" : [2,2],
        "3" : [3,1],
        "4" : [4,0],
        "5" : [6,1],
        "6" : [7,0],
        "7" : [9,2],
        "8" : [10,0],
        "9" : [12,1],
        "10": [13,0],
        "11": [15,2]
    }

    # get joint

    # start robot
    artus.connect()

    # close d1/d2 for thumb
    artus.hard_close(2,0)

    time.sleep(1)

    artus.reset(0,0)

    time.sleep(0.5)

    artus.disconnect()


if __name__ == "__main__":
    # gete com port
    comport = input("Please enter the USB Device COM Port: ")
    try:
        main(comport)
    except Exception as e:
        print('Error = '+e)