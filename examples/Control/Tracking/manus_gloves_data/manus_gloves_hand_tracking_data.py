
import re

import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# TCPServer used for receiving data from unity
from tcp_server.tcp_server import TCPServer

class ManusGlovesHandTrackingData:
    def __init__(self,
                 port=65432):
        self.tcp_server = TCPServer(port=port)
        self.tcp_server.create()

        self.joint_angles_dict_R = {'index':[0,0,0,0],
                                  'middle':[0,0,0,0],
                                  'ring':[0,0,0,0],
                                  'pinky':[0,0,0,0],
                                  'thumb':[0,0,0,0],
                                  }
        
        self.joint_angles_dict_L = {'index':[0,0,0,0],
                                  'middle':[0,0,0,0],
                                  'ring':[0,0,0,0],
                                  'pinky':[0,0,0,0],
                                  'thumb':[0,0,0,0],
                                  }
        
        self.data_l = None
        self.data_r =  None
           
    def get_finger_joint_rotations(self, hand="L"):
            
        # Hand can take these values: L, R, LR

        # Make sure we are not accessing outside of data range
        data = []
        # received_data = self.tcp_server.receive()
        # data = self._extract_data_cpp_api(data_raw=received_data)
        
        # while len(data) < 40:
        received_data = self.tcp_server.receive()
        
        # print(received_data)
        # self.data_l = None
        # self.data_r =  None


        
        
        # print("Received Data: ")
        # print(received_data)
        # while self.data_l == None or self.data_r == None:
            # print("getting data ...")
        # received_data = self.tcp_server.receive()
        if received_data == None:
            # print("left hand: ", self.joint_angles_dict_L)
            # print("right hand: ", self.joint_angles_dict_R)
            return self.joint_angles_dict_L, self.joint_angles_dict_R
         
        temp_l, temp_r = self._extract_between_L_R_manus(s=received_data)
        # print(f"temp_l: {temp_l}")
        # print(f"temp_r: {temp_r}")
        if temp_l != None:
            self.data_l = temp_l
        if temp_r != None:
            self.data_r = temp_r
        print("DataL: ", self.data_l)
        print("self.data_r:", self.data_r)

        extracted_data = self._extract_data_cpp_api(data_raw=self.data_l)
        # print("1")

        # print(f"Extracted data: {extracted_data}")
        # print(extracted_data)
        data.extend(extracted_data)  # Append the extracted data to the data list
        # print("2")

        # print(f"data1: {data}")
        
        extracted_data = self._extract_data_cpp_api(data_raw=self.data_r)
        # print(extracted_data)
        data.extend(extracted_data)  # Append the extracted data to the data list
        # print("3")

        # print(data)

            # print(f"data2: {data}")

        # # data = data.replace(")", "")
        # data = data.split(",")
        # # convert string to int list, ignore the last element
        # data = self._string_to_int_list(data[0:-1])
        # check joint limits
        # data = self._check_joint_limits(data)
        # fill joint angles dict for cpp api
        # print(data)
        self.joint_angles_dict_L['thumb'] = data[0:4]
        self.joint_angles_dict_L['index'] = data[4:8]
        self.joint_angles_dict_L['middle'] = data[8:12]
        self.joint_angles_dict_L['ring'] = data[12:16]
        self.joint_angles_dict_L['pinky'] = data[16:20]
        # self.joint_angles_dict['thumb'] = data[16:20]
        # print(self.joint_angles_dict_L['thumb'])
        
        self.joint_angles_dict_L['thumb'][1] = (70-self.joint_angles_dict_L['thumb'][1])

        # map joint angles
        self.joint_angles_dict_L['index'] = self.joint_angles_mapper(self.joint_angles_dict_L['index'])
        self.joint_angles_dict_L['middle'] = self.joint_angles_mapper(self.joint_angles_dict_L['middle'])
        self.joint_angles_dict_L['pinky'] = self.joint_angles_mapper(self.joint_angles_dict_L['pinky'])
        self.joint_angles_dict_L['ring'] = self.joint_angles_mapper(self.joint_angles_dict_L['ring'])
        self.joint_angles_dict_L['thumb'] = self.joint_angles_mapper(self.joint_angles_dict_L['thumb'])

        # switch angles for thumb abduction
        # temp = self.joint_angles_dict['thumb'][0]
        # self.joint_angles_dict['thumb'][0] = self.joint_angles_dict['thumb'][1]
        # # self.joint_angles_dict['thumb'][1] = temp
        # self.joint_angles_dict['thumb'][1] = self.joint_angles_dict['thumb'][2]
        # self.joint_angles_dict['thumb'][2] = self.joint_angles_dict['thumb'][3]

        self.joint_angles_dict_R['thumb'] = data[20:24]
        self.joint_angles_dict_R['index'] = data[24:28]
        self.joint_angles_dict_R['middle'] = data[28:32]
        self.joint_angles_dict_R['ring'] = data[32:36]
        self.joint_angles_dict_R['pinky'] = data[36:40]
        # self.joint_angles_dict['thumb'] = data[16:20]
        self.joint_angles_dict_R['thumb'][1] = (70-self.joint_angles_dict_R['thumb'][1])

        # map joint angles
        self.joint_angles_dict_R['index'] = self.joint_angles_mapper(self.joint_angles_dict_R['index'])
        self.joint_angles_dict_R['middle'] = self.joint_angles_mapper(self.joint_angles_dict_R['middle'])
        self.joint_angles_dict_R['pinky'] = self.joint_angles_mapper(self.joint_angles_dict_R['pinky'])
        self.joint_angles_dict_R['ring'] = self.joint_angles_mapper(self.joint_angles_dict_R['ring'])
        self.joint_angles_dict_R['thumb'] = self.joint_angles_mapper(self.joint_angles_dict_R['thumb'])

        if hand == "L":
                return self.joint_angles_dict_L
        elif hand == "R":
                return self.joint_angles_dict_R
        elif hand == "LR":
                # print("left hand out: ", self.joint_angles_dict_L)
                # print("right hand out: ", self.joint_angles_dict_R)
                return self.joint_angles_dict_L, self.joint_angles_dict_R
                

    def _extract_between_orientation_and_end(self,s):
        '''
        example data -> SkeletonType: ManusHand_R orientation: 0,0,0,360,0,0,0,0,0,0,0,360,0,0,0,0,0,359,0,0,0,360,0,0,0,360,0,360,0,0,0,0,0,290,0,360,0,360,end
        '''
        pattern = r'orientation:(.*?)end'
        match = re.search(pattern, s, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def _extract_between_L_R_manus(self,s):
        '''
        example data -> SkeletonType: ManusHand_R orientation: 0,0,0,360,0,0,0,0,0,0,0,360,0,0,0,0,0,359,0,0,0,360,0,0,0,360,0,360,0,0,0,0,0,290,0,360,0,360,end
        '''
        pattern_L = None
        pattern_R = None
        pattern_L_pattern = r'L\[(.*?)\]'
        pattern_R_pattern = r'R\[(.*?)\]'

        match_L = re.search(pattern_L_pattern, s, re.DOTALL)
        if match_L:
            pattern_L = match_L.group(1).strip()
        match_R = re.search(pattern_R_pattern, s, re.DOTALL)
        if match_R:
            pattern_R = match_R.group(1).strip()

        return pattern_L, pattern_R
    
    def _extract_data_cpp_api(self, data_raw):
        """
        format: [10.98 57.29 56.76 82.16 -4.91 99.94 55.7 34.87 -9.36 69.46 97.08 61.7 11.68 -18.59 13.95 8.53 18.3 -5.36 0 0 ]
        """
        # print(data_raw
        # data = data_raw.replace("[","").replace("]","").split(" ")[0:-1]
        data = data_raw.replace("[","").replace("]","").split()
        # print(data)
        # data = [int(float(angle)) for angle in data]

        try:
            data = [int(float(angle)) for angle in data]
        except ValueError as e:
            print(f"Error converting data: {e}")
            data = []
        # print(data)
        return data
    
    def _string_to_int_list(self, string_list):
        return [int(element) for element in string_list]
    

    def _check_joint_limits(self, data):

        for i in range(len(data)):
            if (data[i] > 270):
                data[i] = 0
            if (data[i] > 90):
                data[i] = 90
        return data
    
    
    def joint_angles_mapper(self, joint_angles=None):
        # # Ensure joint_angles is not None and is a list
        # if joint_angles is None:
        #     return []
        
        # for i in range(len(joint_angles)):
        #     # Normalize angle to range [-180, 180]
        #     angle = joint_angles[i] % 360
        #     if angle > 180:  # Adjust angles greater than 180 to be in the range of [-180, 0)
        #         angle -= 360

        #     # if i!=0:
        #     angle = -angle
        #     joint_angles[i] = angle

        return joint_angles


def main():
    hand_tracking_data = ManusGlovesHandTrackingData()
    while True:
        try:
            data = hand_tracking_data.get_finger_joint_rotations(hand="LR")
            # print("Dictionary: ")
            # print(data)
            if data:
                # print("index: ", data['index'])
                # print("middle: ", data['middle'])
                # print("ring: ", data['ring'])
                # print("pinky: ", data['pinky'])
                # print("thumb: ", data['thumb'])
                print()

        except:
            pass
        time.sleep(0.1)


if __name__ == "__main__":
    main()