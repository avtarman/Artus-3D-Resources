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

def unjam():
    # Initialize ArtusAPI with specified parameters
    artus = ArtusAPI(
        communication_method='UART',
        communication_channel_identifier='/dev/ttyUSB0',
        robot_type='artus_lite',
        hand_type='right',
        reset_on_start=0
    )
    
    # Connect to the hand
    artus.connect()
    time.sleep(0.3)  # 100ms delay

    # Hard close sequence for specific joints
    joints = [0, 2, 4, 6, 7, 10, 13, 15]
    for j in joints:
        artus.hard_close(j=j, m=0)
        time.sleep(0.3)  # Small delay between commands

    print('Unjam complete, starting calibration')
    time.sleep(3)

    artus.calibrate()

    return artus

if __name__ == "__main__":
    if input('Are you sure you want to unjam the hand? ALL JOINTS MUST BE COMPLETELY OPEN (y/n): ') == 'y':
        unjam()

