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
print(desired_path)

from ArtusAPI.artus_api import ArtusAPI

def example():
    with open(os.path.join(desired_path,'data','hand_poses','grasp_example.json'),'r') as file:
        grasp_dict = json.load(file)
    artusapi = ArtusAPI(communication_method='WiFi',hand_type='right',communication_channel_identifier='ArtusMK6RH',stream=True,communication_frequency=10)

    artusapi.connect()
    artusapi.wake_up()
    while True:
        # artusapi.set_joint_angles(grasp_dict)
        print(artusapi.get_streamed_joint_angles())
        # time.sleep(0.1)


if __name__ == '__main__':
    example()


