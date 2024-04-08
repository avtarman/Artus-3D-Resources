import time
import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from Artus3DAPI import Artus3DAPI,UART,WIFI

MK5LH = 'ArtusMK6LH'
sleep = 0.5
artus = Artus3DAPI(target_ssid=MK5LH,communication_method=UART,port='COM11',hand='left')

artus.start_connection()
time.sleep(1)
inp = input("Is this first start (new power cycle)? (Y/N) ")
if inp == 'Y' or inp =='y':
    artus.start_robot()
time.sleep(sleep)

for joint,joint_stuff in artus.joints.items():
    joint_stuff.input_speed = 90

while True:

    # finger wave down
    time.sleep(5)
    artus.joints['pinky_flex'].input_angle = 80
    artus.joints['pinky_d2'].input_angle = 60
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['ring_flex'].input_angle = 80
    artus.joints['ring_d2'].input_angle = 60
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['middle_flex'].input_angle = 80
    artus.joints['middle_d2'].input_angle = 60
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['index_flex'].input_angle = 80
    artus.joints['index_d2'].input_angle = 60
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['thumb_flex'].input_angle = 80
    artus.joints['thumb_d1'].input_angle = 60
    artus.joints['thumb_d2'].input_angle = 60
    
    artus.send_target_command()
    time.sleep(2)

    # finger wave up
    artus.joints['thumb_flex'].input_angle = 00
    artus.joints['thumb_d1'].input_angle = 00
    artus.joints['thumb_d2'].input_angle = 00
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['index_flex'].input_angle = 00
    artus.joints['index_d2'].input_angle = 00
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['middle_flex'].input_angle = 00
    artus.joints['middle_d2'].input_angle = 00
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['ring_flex'].input_angle = 00
    artus.joints['ring_d2'].input_angle = 00
    artus.send_target_command()
    time.sleep(sleep)
    artus.joints['pinky_flex'].input_angle = 00
    artus.joints['pinky_d2'].input_angle = 00
    artus.send_target_command()
    time.sleep(sleep)

    time.sleep(5)

    # spock
    artus.joints['middle_flex'].input_angle = 5
    artus.joints['index_flex'].input_angle = 5
    artus.joints['ring_flex'].input_angle = 5
    artus.joints['pinky_flex'].input_angle = 5

    artus.joints['index_spread'].input_angle = -5
    artus.joints['middle_spread'].input_angle = -8

    artus.joints['ring_spread'].input_angle = 8
    artus.joints['pinky_spread'].input_angle = 5

    artus.joints['thumb_flex'].input_angle = 50
    artus.joints['thumb_spread'].input_angle = -20
    artus.joints['thumb_d1'].input_angle = 40
    artus.joints['thumb_d2'].input_angle = 40

    artus.send_target_command()

    time.sleep(5)

    # home 
    for name,joint in artus.joints.items():
        joint.input_angle = 0

    artus.send_target_command()

    time.sleep(5)
