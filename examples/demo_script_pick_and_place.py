import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from artus_3d_api.Artus3DAPI import Artus3DAPI,UART,WIFI



if __name__ == '__main__':
    artus = Artus3DAPI(port='/dev/ttyUSB0',communication_method=UART)

    artus.start_connection()

    time.sleep(0.01)

    artus.start_robot()

    while True:
        input_ = input('1 to close, 2 to open')

        if input_ == '1':
            for joint,joint_stuff in artus.joints.items():
                joint_stuff.input_speed = 95

            artus.joints['thumb_flex'].input_angle = 80
            artus.send_target_command()
            time.sleep(0.01)

            artus.joints['index_flex'].input_angle = 75
            artus.joints['middle_flex'].input_angle = 75

            artus.send_target_command()
            time.sleep(0.01)

            artus.joints['middle_d2'].input_angle = 50
            artus.joints['index_d2'].input_angle = 50

            artus.send_target_command()
            time.sleep(0.01)

        elif input_ == '2':
            for joint,joint_stuff in artus.joints.items():
                joint_stuff.input_speed = 90

            artus.joints['thumb_flex'].input_angle = 20
            artus.send_target_command()
            time.sleep(0.01)

            artus.joints['index_flex'].input_angle = 20
            artus.joints['middle_flex'].input_angle = 20

            artus.send_target_command()
            time.sleep(0.01)

            artus.joints['middle_d2'].input_angle = 00
            artus.joints['index_d2'].input_angle = 00

            artus.send_target_command()
            time.sleep(0.01)




