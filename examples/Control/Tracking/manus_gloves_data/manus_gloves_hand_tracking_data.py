
import re
import numpy as np
import threading
from collections import deque


import time



from pathlib import Path
import sys
current_file_path = Path(__file__).resolve()
PROJECT_ROOT = current_file_path.parents[4]
print("Root: ",PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)
from RMD_Actuator_Control.RMD_Actuator_Control.Application.helpers.Path_Smoothener.moving_average import MultiMovingAverage

class ManusHandTrackingData:

    def __init__(self,
                 port=65432):
        
        self.port = port


        self.order_of_joints = ['index', 'middle', 'ring', 'pinky', 'thumb']
        self.running = False
        self.data_queue = {'index': deque(maxlen=20), 'middle': deque(maxlen=20), 'ring': deque(maxlen=20), 'pinky': deque(maxlen=20), 'thumb': deque(maxlen=20)}
        self.user_hand_min_max_left = {'index': [-15,15,0,90,0,90], 'middle': [-15,15,0,90,0,90], 'ring': [-15,15,0,90,0,90], 'pinky': [-15,15,0,90,0,90], 'thumb': [-25,25,0,90,0,90,0,90]}
        self.user_hand_min_max_right = {'index': [-15,15,0,90,0,90], 'middle': [-15,15,0,90,0,90], 'ring': [-15,15,0,90,0,90], 'pinky': [-15,15,0,90,0,90], 'thumb': [-25,25,0,90,0,90,0,90]}
        self.artus_min_max = {'index': [-15,15,0,90,0,90], 'middle': [-15,15,0,90,0,90], 'ring': [-15,15,0,90,0,90], 'pinky': [-15,15,0,90,0,90], 'thumb': [-25,25,0,90,0,90,0,90]}

        
        self.moving_average_righthand = MultiMovingAverage(window_size=10, num_windows=20)
        self.moving_average_lefthand = MultiMovingAverage(window_size=10, num_windows=20)


        self.hand_tracking

        self.joint_angles_left = None # [thumb_1, thumb_2, thumb_3, thumb4, index_1, index_2, index_3, middle_1, middle_2, middle_3, ring, pinky]
        self.joint_angles_right = None

    # def get_tcp_port_handle(self):
    #     pass

    
    def receive_joint_angles(self):
        """
        Receive joint angles from the hand tracking method
        """
        joint_angles = self.tcp.receive() # receive encoded data
        if joint_angles == None:
            return None
        self._joint_angles_gui_to_joint_streamer(joint_angles)
        return joint_angles
    
    def get_left_hand_joint_angles(self):
        return self.joint_angles_left
    
    def get_right_hand_joint_angles(self):
        return self.joint_angles_right
    
    def _joint_angles_manus_to_joint_streamer(joint_angles)
        
        # decode left and right  and put it in the joint_angles_left variable
        self.joint_angles_left = 
        self.joint_angles_right = 
        
        return self.joint_angles_left, self.joint_angles_right

        

    def get_finger_joint_rotations_dict(self, hand):
        # time.sleep(0.01)
        return self.hand_tracking.get_finger_joint_rotations(hand)
    
    # def get_finger_joint_rotations_list(self):
    #     joint_rotations_dict = self.get_finger_joint_rotations_dict()
    #     joint_rotations_list = []
    #     for finger in self.order_of_joints:
    #         joint_rotations_list += joint_rotations_dict[finger]
    #     return joint_rotations_list
    
    def get_finger_joint_rotations_list_rad(self, hand="L"):

        # Hand can take these values: L, R, LR
    
        joint_rotations_dict_L = []
        joint_rotations_dict_R = []
        joint_rotations_list_L = []
        joint_rotations_list_R = []

        if hand == "L":
            joint_rotations_dict_L = self.get_finger_joint_rotations_dict(hand)
            self.interpolate_data_L(joint_rotations_dict_L)
            self.append_list_L(joint_rotations_dict_L, joint_rotations_list_L)

            joint_rotations_list_L = np.deg2rad(joint_rotations_list_L)

            return joint_rotations_list_L
        
        elif hand == "R":
            joint_rotations_dict_R = self.get_finger_joint_rotations_dict(hand)
            self.interpolate_data_R(joint_rotations_dict_R)
            self.append_list_R(joint_rotations_dict_R, joint_rotations_list_R)

            joint_rotations_list_R = np.deg2rad(joint_rotations_list_R)

            return joint_rotations_list_R
        elif hand == "LR":
            joint_rotations_dict_L, joint_rotations_dict_R = self.get_finger_joint_rotations_dict(hand)
            self.interpolate_data_L(joint_rotations_dict_L)
            self.interpolate_data_R(joint_rotations_dict_R)
            self.append_list_L(joint_rotations_dict_L, joint_rotations_list_L)
            self.append_list_R(joint_rotations_dict_R, joint_rotations_list_R)

            joint_rotations_list_L = np.deg2rad(joint_rotations_list_L)
            joint_rotations_list_R = np.deg2rad(joint_rotations_list_R)
            
            print("joint rotations isaac sim: ", joint_rotations_list_L, joint_rotations_list_R)

            return joint_rotations_list_L, joint_rotations_list_R
    
    def append_list_L(self, joint_rotations_dict, joint_rotations_list):
        joint_rotations_list.append(joint_rotations_dict['index'][0])
        joint_rotations_list.append(joint_rotations_dict['middle'][0])
        joint_rotations_list.append(joint_rotations_dict['pinky'][0])
        joint_rotations_list.append(joint_rotations_dict['ring'][0])
        joint_rotations_list.append(-joint_rotations_dict['thumb'][0])

        joint_rotations_list.append(joint_rotations_dict['index'][1])
        joint_rotations_list.append(joint_rotations_dict['middle'][1])
        joint_rotations_list.append(joint_rotations_dict['pinky'][1])
        joint_rotations_list.append(joint_rotations_dict['ring'][1])
        joint_rotations_list.append(joint_rotations_dict['thumb'][1])
        
        joint_rotations_list.append(joint_rotations_dict['index'][2])
        joint_rotations_list.append(joint_rotations_dict['middle'][2])
        joint_rotations_list.append(joint_rotations_dict['pinky'][2])
        joint_rotations_list.append(joint_rotations_dict['ring'][2])
        joint_rotations_list.append(joint_rotations_dict['thumb'][2])
        
        joint_rotations_list.append(joint_rotations_dict['index'][2])
        joint_rotations_list.append(joint_rotations_dict['middle'][2])
        joint_rotations_list.append(joint_rotations_dict['pinky'][2])
        joint_rotations_list.append(joint_rotations_dict['ring'][2])
        joint_rotations_list.append(joint_rotations_dict['thumb'][3])

        # add joint positions to moving average handler
        self.moving_average_lefthand.add_values(joint_rotations_list.copy())
        # get the average of the joint positions
        joint_rotations_list = self.moving_average_lefthand.get_averages()

    def append_list_R(self, joint_rotations_dict, joint_rotations_list):
        joint_rotations_list.append(joint_rotations_dict['index'][0])
        joint_rotations_list.append(joint_rotations_dict['middle'][0])
        joint_rotations_list.append(joint_rotations_dict['pinky'][0])
        joint_rotations_list.append(joint_rotations_dict['ring'][0])
        joint_rotations_list.append(-joint_rotations_dict['thumb'][0])

        joint_rotations_list.append(joint_rotations_dict['index'][1])
        joint_rotations_list.append(joint_rotations_dict['middle'][1])
        joint_rotations_list.append(joint_rotations_dict['pinky'][1])
        joint_rotations_list.append(joint_rotations_dict['ring'][1])
        joint_rotations_list.append(joint_rotations_dict['thumb'][1])
        
        joint_rotations_list.append(joint_rotations_dict['index'][2])
        joint_rotations_list.append(joint_rotations_dict['middle'][2])
        joint_rotations_list.append(joint_rotations_dict['pinky'][2])
        joint_rotations_list.append(joint_rotations_dict['ring'][2])
        joint_rotations_list.append(joint_rotations_dict['thumb'][2])
        
        joint_rotations_list.append(joint_rotations_dict['index'][2])
        joint_rotations_list.append(joint_rotations_dict['middle'][2])
        joint_rotations_list.append(joint_rotations_dict['pinky'][2])
        joint_rotations_list.append(joint_rotations_dict['ring'][2])
        joint_rotations_list.append(joint_rotations_dict['thumb'][3])
        
        # add joint positions to moving average handler
        self.moving_average_righthand.add_values(joint_rotations_list.copy())
        # get the average of the joint positions
        joint_rotations_list = self.moving_average_righthand.get_averages()
    
    
    # def get_hand_orientation(self):
    #     return self.hand_tracking.get_hand_orientation()
    
    # def get_hand_position(self):
    #     return self.hand_tracking.get_hand_position()
    
    def scale_value(self, value, min_val, max_val, arm_min_val, arm_max_val):
        # Ensure the value is within the min_max range
        value = max(min_val, min(value, max_val))

        # Map the value to the artus
        if max_val - min_val == 0:
            return arm_min_val  # Avoid division by zero if min_val == max_val

        scaled_value = ((value - min_val) / (max_val - min_val)) * (arm_max_val - arm_min_val) + arm_min_val
        return scaled_value
    
    def interpolate_data_L(self, joint_rotations_list):
        for finger in self.order_of_joints:
            num_joints = 0
            if finger == "thumb":
                num_joints = 4
            else:
                num_joints = 3

            for joint_index in range(num_joints):
                value = joint_rotations_list[finger][joint_index]
                min_index = joint_index * 2
                max_index = min_index + 1

                min_val = self.min_max_L[finger][min_index]
                max_val = self.min_max_L[finger][max_index]
                arm_min_val = self.artus_min_max[finger][min_index]
                arm_max_val = self.artus_min_max[finger][max_index]

                scaled_value = self.scale_value(value, min_val, max_val, arm_min_val, arm_max_val)
                joint_rotations_list[finger][joint_index] = scaled_value

        return joint_rotations_list
    
    def interpolate_data_R(self, joint_rotations_list):
        for finger in self.order_of_joints:
            num_joints = 0
            if finger == "thumb":
                num_joints = 4
            else:
                num_joints = 3

            for joint_index in range(num_joints):
                value = joint_rotations_list[finger][joint_index]
                min_index = joint_index * 2
                max_index = min_index + 1

                min_val = self.min_max_R[finger][min_index]
                max_val = self.min_max_R[finger][max_index]
                arm_min_val = self.artus_min_max[finger][min_index]
                arm_max_val = self.artus_min_max[finger][max_index]

                scaled_value = self.scale_value(value, min_val, max_val, arm_min_val, arm_max_val)
                joint_rotations_list[finger][joint_index] = scaled_value

        return joint_rotations_list
    
    def gather_data_L(self):
        while self.running:
            current_data = self.get_finger_joint_rotations_dict(hand="L")
            for finger in self.order_of_joints:
                self.temp[finger] = current_data[finger]
            time.sleep(0.1)

    def gather_data_R(self):
        while self.running:
            current_data = self.get_finger_joint_rotations_dict(hand="R")
            # print("Current data: ", current_data)
            for finger in self.order_of_joints:
                self.temp[finger] = current_data[finger]
            time.sleep(0.1)

    def get_data(self, hand):
        self.running = True
        if hand == "L":
            thread = threading.Thread(target=self.gather_data_L)
        elif hand == "R":
            thread = threading.Thread(target=self.gather_data_R)            
        thread.start()

        print()
        input("Press Enter to record value")
        print()

        self.running = False
        thread.join()  # Wait for the thread to finish

    def calibrate_L(self):

        ############# Calibrating Finger Spread ###########################
        for finger in self.order_of_joints:

            ###################### MIN ############################

            print(f"Calibrating LEFT {finger} SPREAD MIN")
            self.get_data("L")
            self.min_max_L[finger][0] = self.temp[finger][0]

            ###################### MAX ############################

            print(f"Calibrating LEFT {finger} SPREAD MAX")
            self.get_data("L")
            self.min_max_L[finger][1] = self.temp[finger][0]


        ############# Calibrating Finger Flex ###########################
        print(f"Put LEFT fingers together flat on table, thumb outwards (Making L shape)")
        self.get_data("L")

        # self.order_of_joints = ['index', 'middle', 'ring', 'pinky', 'thumb']

        self.min_max_L["index"][2] = self.temp["index"][1]
        self.min_max_L["middle"][2] = self.temp["middle"][1]
        self.min_max_L["ring"][2] = self.temp["ring"][1]
        self.min_max_L["pinky"][2] = self.temp["pinky"][1]
        self.min_max_L["thumb"][2] = self.temp["thumb"][1]

        self.min_max_L["index"][4] = self.temp["index"][2]
        self.min_max_L["middle"][4] = self.temp["middle"][2]
        self.min_max_L["ring"][4] = self.temp["ring"][2]
        self.min_max_L["pinky"][4] = self.temp["pinky"][2]
        self.min_max_L["thumb"][4] = self.temp["thumb"][2]

        self.min_max_L["thumb"][6] = self.temp["thumb"][3]

        print(f"Bend fingers 90 degrees")
        self.get_data("L")

        # self.order_of_joints = ['index', 'middle', 'ring', 'pinky', 'thumb']

        self.min_max_L["index"][3] = self.temp["index"][1]
        self.min_max_L["middle"][3] = self.temp["middle"][1]
        self.min_max_L["ring"][3] = self.temp["ring"][1]
        self.min_max_L["pinky"][3] = self.temp["pinky"][1]

        print(f"Fully bend four fingers")
        self.get_data("L")

        self.min_max_L["index"][5] = self.temp["index"][2]
        self.min_max_L["middle"][5] = self.temp["middle"][2]
        self.min_max_L["ring"][5] = self.temp["ring"][2]
        self.min_max_L["pinky"][5] = self.temp["pinky"][2]

        ############# Calibrating Thumb Flex ###########################
        print(f"Move thumb to the bottom of pinky")
        self.get_data("L")

        self.min_max_L["thumb"][3] = self.temp["thumb"][1]

        print(f"Curl Thumb")
        self.get_data("L")

        self.min_max_L["thumb"][5] = self.temp["thumb"][2]
        self.min_max_L["thumb"][7] = self.temp["thumb"][3]

        # print(self.min_max_L)
        return self.min_max_L
     

    def calibrate_R(self):

        ############# Calibrating Finger Spread ###########################
        for finger in self.order_of_joints:

            ###################### MIN ############################

            print(f"Calibrating RIGHT {finger} SPREAD MIN")
            self.get_data("R")
            self.min_max_R[finger][0] = self.temp[finger][0]

            ###################### MAX ############################

            print(f"Calibrating RIGHT {finger} SPREAD MAX")
            self.get_data("R")
            self.min_max_R[finger][1] = self.temp[finger][0]


        ############# Calibrating Finger Flex ###########################
        print(f"Put RIGHT fingers together flat on table, thumb outwards (Making L shape)")
        self.get_data("R")

        self.min_max_R["index"][2] = self.temp["index"][1]
        self.min_max_R["middle"][2] = self.temp["middle"][1]
        self.min_max_R["ring"][2] = self.temp["ring"][1]
        self.min_max_R["pinky"][2] = self.temp["pinky"][1]
        self.min_max_R["thumb"][2] = self.temp["thumb"][1]

        self.min_max_R["index"][4] = self.temp["index"][2]
        self.min_max_R["middle"][4] = self.temp["middle"][2]
        self.min_max_R["ring"][4] = self.temp["ring"][2]
        self.min_max_R["pinky"][4] = self.temp["pinky"][2]
        self.min_max_R["thumb"][4] = self.temp["thumb"][2]

        self.min_max_R["thumb"][6] = self.temp["thumb"][3]

        print(f"Bend fingers 90 degrees")
        self.get_data("R")

        self.min_max_R["index"][3] = self.temp["index"][1]
        self.min_max_R["middle"][3] = self.temp["middle"][1]
        self.min_max_R["ring"][3] = self.temp["ring"][1]
        self.min_max_R["pinky"][3] = self.temp["pinky"][1]

        print(f"Fully bend four fingers")
        self.get_data("R")

        self.min_max_R["index"][5] = self.temp["index"][2]
        self.min_max_R["middle"][5] = self.temp["middle"][2]
        self.min_max_R["ring"][5] = self.temp["ring"][2]
        self.min_max_R["pinky"][5] = self.temp["pinky"][2]

        ############# Calibrating Thumb Flex ###########################
        print(f"Move thumb to the bottom of pinky")
        self.get_data("R")

        self.min_max_R["thumb"][3] = self.temp["thumb"][1]

        print(f"Curl Thumb")
        self.get_data("R")

        self.min_max_R["thumb"][5] = self.temp["thumb"][2]
        self.min_max_R["thumb"][7] = self.temp["thumb"][3]

        # print(self.min_max_R)
        return self.min_max_R

    def use_calibrated_data(self, data, hand):
        if hand == 'L':
            self.min_max_L = data
        else:
            self.min_max_R = data



def test_hand_tracking_data():
    hand_tracking_data = ManusGlovesHandTrackingData(port=65432)
    while True:
        # Receive joint angles from Manus core exe
        joint_angles = hand_tracking_data.receive_joint_angles()

        if joint_angles is not None:
            # left and right hand joitn angles for the application 
            joint_angles_left = hand_tracking_data.get_left_hand_joint_angles()
            joint_angles_right = hand_tracking_data.get_right_hand_joint_angles()
            print("Left Hand Data: ", joint_angles_left)
            print("Right Hand Data: ", joint_angles_right)


if __name__ == "__main__":
    test_hand_tracking_data()