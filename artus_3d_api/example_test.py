import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI,UART,WIFI

if __name__ == '__main__':
    artus = Artus3DAPI(communication_method=UART,port='/dev/ttyUSB1',hand='right')

    artus.start_connection()
    artus.start_robot()

    step = 30
    direction_flag = 1

    for i in range(len(artus.joint_names)):
        if 'spread' in artus.joint_names[i]:
            continue
        else:
            time.sleep(2)
            artus.joints[artus.joint_names[i]].input_speed = 96
        while direction_flag is not None:
            if direction_flag == 1:
                artus.joints[artus.joint_names[i]].input_angle += step
                # reverse direction
                if artus.joints[artus.joint_names[i]].input_angle == 90:
                    direction_flag = 0
            else:
                artus.joints[artus.joint_names[i]].input_angle -= step
                # end loop
                if artus.joints[artus.joint_names[i]].input_angle == 0:
                    direction_flag = None
            artus.send_target_command()
            time.sleep(1)
        # reset dir flag
        direction_flag = 1