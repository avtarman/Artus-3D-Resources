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

def unjam(comport):
    # Initialize ArtusAPI with specified parameters
    artus = ArtusAPI(
        communication_method='UART',
        communication_channel_identifier=comport,
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
        time.sleep(0.5)  # Small delay between commands
        print('Running joint')

    print('unjame complete')
    time.sleep(3)

    artus.disconnect()

    return

def set_reset_on_start(comport):
    # Initialize ArtusAPI with specified parameters
    artus = ArtusAPI(
        communication_method='UART',
        communication_channel_identifier=comport,
        robot_type='artus_lite',
        hand_type='right',
        reset_on_start=1
    )

    artus.connect()

    time.sleep(3)
    if input('Do you want to calibrate? (y/n) :') == 'y':
        artus.calibrate()

    print('finished')

if __name__ == "__main__":
    com = input('Please enter COM Port of device (e.g. COM3) : ')
    if input('Are you sure you want to unjam the hand? ALL JOINTS SHOULD BE COMPLETELY OPEN (y/n): ') == 'y':
        unjam(com)
        if input('have all joints moved? y/n: ') == 'y':
            set_reset_on_start(com)

