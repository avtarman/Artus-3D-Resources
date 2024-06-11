"""
Artus 3D API created for the Artus 3D
Sarcomere Dynamics Inc.

"""

# imports
import time
import json
import logging

import os
import sys
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from artus_lite_api.src.python_server import PythonServer
from artus_lite_api.src.python_uart import PythonEsp32Serial
from artus_lite_api.src.ArtusLiteJoint import ArtusLiteJoint
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from RMD_Actuator_Control.RMD_Actuator_Control.data_pipeline.zmq_utils import zmqUtils
from RMD_Actuator_Control.RMD_Actuator_Control.data_pipeline_timer.zmq_utils_alternate import zmqUtils_alternate

# Constants
WIFI = 'WiFi'
UART = 'UART'


class ArtusAPI:
    def __init__(self,
                 communication_method = 'WiFi',
                 port='COM9',
                 target_ssid = 'Artus3DTester',
                 hand = 'right',
                 zmq_ = False
                 ):
        
        self.target_ssid = target_ssid
        self.communication_method = communication_method
        self.port = port
        self.hand = hand
        self.zmq = zmq_

        # command codes
        self.target_cmd = '176'
        self.execute_grasp_cmd = '250'
        self.calibrate_cmd = '055'
        self.start_cmd = '088'
        self.getstates_cmd = '010'
        self.sleep_cmd = '025'
        self.save_grasp_cmd ='200'
        self.get_grasps_cmd = '210'
        self.execute_grasp_cmd = '250'
        self.empty_message = "[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"

        # placeholders for values
        self.command = 0
        self.default_velocity = 90
        self.joint_names = ['thumb_flex','thumb_spread','thumb_d2','thumb_d1','index_flex','index_spread','index_d2',
                        'middle_flex','middle_spread','middle_d2','ring_flex','ring_spread','ring_d2','pinky_flex',
                        'pinky_spread','pinky_d2']
        
        # temporary dictionaries for constraints, joint parameters to be set and joint states to be read
        constraints = {
            'max':[90,30,90,90,90,15,90,90,15,90,90,15,90,90,15,90],
            'min':[0,-30,0,0,0,-15,0,0,-15,0,0,-15,0,0,-15,0]
        }

        if self.zmq == True:
            # self.zmq = zmqUtils(source="Artus", streaming_freq= 15)
            self.zmq = zmqUtils_alternate(source="Artus")
            

        self.joints = {}
        
        self.joint_commands = [0]*len(self.joint_names)
        self.joint_feedback = [0]*len(self.joint_names)

        for i,joint in enumerate(self.joint_names):
            self.joints[joint] = ArtusLiteJoint(joint,i,constraints['max'][i],constraints['min'][i])

        self.robot_command = self.grasp_pattern = None
        
        # instantiate server and serial classes
        self.python_server = PythonServer(reqReturnFlag = False,target_ssid=self.target_ssid)
        self.python_serial = PythonEsp32Serial(port=self.port)

    '''
    Getters for variables
    '''
    def get_joint(self,joint_name):
        return self.joints[joint_name]

    '''
    Start the connection to the Robot Hand and send the Robot Hand a start command
    '''
    def start_connection(self):

        # start server in either wifi or UART mode
        if self.communication_method == "WiFi":
            try:
                self.python_server.start()
            except Exception as e:
                logging.error("error starting python server")
                print(e)
                pass

        if self.communication_method == "UART":
            try:
                self.python_serial.start()
                ## clear buffer
                for i in range(self.python_serial.esp32.in_waiting):
                    self.python_serial.receive()
            except Exception as e:
                logging.error("error starting serial connection")
                print(e)
                pass

    '''
    Start the connection
    '''
    def start_robot(self):
        # send start command to the robot
        # set RTC values
        year = str(time.localtime().tm_year - 2000)
        month = str(time.localtime().tm_mon)
        day = str(time.localtime().tm_mday)
        hour = str(time.localtime().tm_hour)
        minute = str(time.localtime().tm_min)
        second = str(time.localtime().tm_sec)

        if int(month) < 10:
            month = '0'+ month
        if int(day) < 10:
            day = '0'+ day
        if int(hour) < 10:
            hour = '0'+ hour
        if int(minute) < 10:    
            minute = '0'+ minute
        if int(second) < 10:
            second = '0'+ second

        self.robot_command = "c088p[20,"+year+","+month+","+day+","+hour+","+minute+","+second+",00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        # send command
        self._send(self.robot_command)
        return self.robot_command
    
    '''
    Close the connection between the server and the Robot Hand
    '''
    def close_connection(self):
        try:
            # retrieve files either over WiFi or UART
            if self.communication_method == "WiFi": # wifi
                self.python_server.close()
                
            elif self.communication_method == "UART": # uart
                self.python_serial.close()
        except Exception as e:
            logging.warning("unable to close connection")

    '''
    Send a target command
    '''
    def send_target_command(self,cmd=None):
        if cmd:
            if self.hand == 'right':
                # find position index
                index = cmd.find('[')
                # create list from string
                string_list = list(cmd)
                index+=1 # increment 1 index for start of position
                # iterate through angles
                for i in range(16):
                    if i in [1,5,8,11,14]: # positions of spreads
                        if abs(int(cmd[index:index+3])) > 0: # only change if absolute value is greater than 0
                            if string_list[index] == '-':
                                string_list[index] = '+'
                            else:
                                string_list[index] = '-'
                    # thumb changes
                    elif i == 2:
                        temp = string_list[index:index+3]
                    elif i == 3:
                        string_list[index-4:index-1] = string_list[index:index+3]
                        string_list [index:index+3] = temp 
                    index += 4
                    
                cmd = ''.join(string_list)
            self._send(cmd)
            return None
        self.command = self.target_cmd

        for joint_name,joint in self.joints.items():
            joint.check_input_constraints()
            if self.hand == 'right':
                if 'spread' in joint_name:
                    joint.input_angle = -joint.input_angle

        # set the command
        self.robot_command = 'c{0}p[{1}]v[{2}]end\n'.format(
            self.command,
            ','.join(str(joint.input_angle) for name,joint in self.joints.items()),
            ','.join(str(joint.input_speed) for name,joint in self.joints.items())
        )
        self.grasp_pattern = 'p[{0}]v[{1}]end\n'.format(
            ','.join(str(joint.input_angle) for name,joint in self.joints.items()),
            ','.join(str(joint.input_speed) for name,joint in self.joints.items())
        )

        self._send(self.robot_command)
        return self.robot_command
    '''
    Update states for Robot Hand
    @param: single item
    '''
    def set_robot_params_by_joint_name(self,name:str,input_angle:int=None,input_speed:int=None):
        if input_angle is not None:
            self.joints[name].input_angle = input_angle
        if input_speed:
            self.joints[name].input_speed = input_speed
        return
    
    '''
    Update states for Robot Hand
    @param: single item
    '''
    # def set_robot_params_by_joint_name(self,index:int,input_angle:int,input_speed:int=None):
    #     for name,joint in self.joints.items():
    #         if joint['joint_index'] == index:
    #             self.joint.input_angle = input_angle
    #         if input_speed:
    #             self.joint.input_speed = input_speed
    #         break
    #     return

    '''
    Get states from Robot Hand
    '''
    def get_robot_states(self):

        self._send("c010p"+self.empty_message)

        start = time.perf_counter()

        while time.perf_counter() - start < 0.0001:
            pass  

        str_return = ''
        while str_return == '':
            str_return = self._receive()

        # print(str_return)
        # if empty Mk5+ compatible
        if "position" in str_return:
            return None,None
        try:
            valid_json_return = str_return.replace("'",'"').replace(" ","")
            valid_json_return = valid_json_return[:(valid_json_return.find(']'))]+"]}"
            

            # valid_json_return = valid_json_return[:47]+"}"
            states_return = json.loads(valid_json_return)

            for name,joint in self.joints.items():
                if 'flex' in name:
                    joint.feedback_angle = int(states_return['p'][joint.joint_index]+(abs(states_return['p'][joint.joint_index+1])/2))
                elif 'spread' in name:
                    joint.feedback_angle = int(states_return['p'][joint.joint_index]/2)
                else:
                    joint.feedback_angle = states_return['p'][joint.joint_index]
                # joint.feedback_current = states_return['c'][joint.joint_index]
                # joint.feedback_temperature = states_return['t'][joint.joint_index]

            print('  |  '.join(f"{name}:{obj.feedback_angle}" for name,obj in self.joints.items()))

        except Exception as e:
            logging.error('Unable to load robot states')

        return self.joints

    '''
    Reset specified actuator finger back to 0 chosen through parameter
    @param: joint - indice from joint map
    @param act - side of motor (dev)
    '''
    def locked_reset_low(self,joint:str,act:str):
        if int(joint) < 10:
            joint = '0'+joint
        self.robot_command = "c012p["+joint+",0"+act+",00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        # send command
        self._send(self.robot_command)
        return self.robot_command

    '''
    Send a target command to the Robot Hand
    '''
    def _send(self, message):
        try:
            # Send Command to Robot based on communication method
            message = self._check_command_string(message)
            if self.communication_method == "WiFi": # wifi
                # message = self._check_command_string(message)
                print(message)
                # return
                self.python_server.send(message)
            elif self.communication_method == "UART": # uart
                print(message)
                self.python_serial.send(message)
        except Exception as e:
            logging.warning("unable to send command")
            print(e)
            pass
    
    '''
    Receive a message from the Robot Hand
    '''
    def _receive(self):
        """
        Recieve Command from Robot
        """
        try:    
            if self.communication_method == "WiFi": # wifi
                message  = self.python_server.receive()

            elif self.communication_method == "UART": # uart
                message  = self.python_serial.receive()
            return message
        except Exception as e:
            logging.warning("unable to receive message")
            print(e)
            return " "
        

    '''
    Calibrate Robot Hand
    '''
    def calibrate(self):
        self.robot_command = 'c'+self.calibrate_cmd+'p'+self.empty_message
        self._send(self.robot_command)

    '''
    Sleep the Robot Hand and save joint positions locally on Robot Hand before powering off to remember state
    '''
    def sleep(self):
        self.robot_command = 'c'+self.sleep_cmd+'p'+self.empty_message
        self._send(self.robot_command)

    '''
    flash Actuator Drivers with onboard bin file
    '''
    def flash_file(self): # only WiFi is configured
        
        while True:
            num = input("Enter STM number (1-8) to flash or press enter to perform a full flash procedure: ")
            if num == '':
                self._send("c099p[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n")
                break
            elif int(num) > 0 and int(num) <= 8:
                self._send("c099p[0"+num+",00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n")
                break
            logging.warning("Invalid input. Please enter a number between 1 and 8 or press enter.")

        if self.communication_method == "WiFi": # wifi
            self.python_server.flash_wifi()
            
        elif self.communication_method == "UART": # uart
            self.python_serial.flash_serial()
    ''' 
    save last executed grasp pattern to SD card on masterboard
    '''
    def save_grasp_pattern(self):
        while True:
            num = input("Enter file num (1-6) to save grasp to")
            if int(num) >= 1 and int(num) <= 6:
                break
            elif num == "":
                break
            logging.warning("Invalid input. Please enter a number between 1 and 6 or press enter.")
        if num =="": return
        save_pos = self.save_grasp_cmd + int(num)
        
        self.robot_command = 'c'+ save_pos + self.grasp_pattern
        print("Saving grasp: ", self.grasp_pattern, ' to file ' + num)
        self._send(self.robot_command)

        # str_return = ''
        # while str_return == '':
        #     str_return = self._receive()
        # print(str_return)
        return self.robot_command

    '''
    Load grasp pattern into self.robot_command from text file
    '''
    def get_grasp_pattern(self,name=None):

        self.robot_command = 'c'+self.get_grasps_cmd+'p'+self.empty_message
        self._send(self.robot_command)
        str_return = ''
        i = 0
        while i < 6:
            str_return = self._receive()
            if str_return !='': 
                print(str_return)
                i+=1
        return 
    
    '''
    Load grasp pattern into self.robot_command from text file
    '''
    def execute_grasp_pattern(self):
        while True:
            num = input("Enter file num (1-6) to execute grasp from")
            if int(num) >= 1 and int(num) <= 6:
                break
            elif num == "":
                break
            logging.warning("Invalid input. Please enter a number between 1 and 6 or press enter.")
        if num =="": return
        grasp_cmd = self.execute_grasp_cmd + int(num)
        self.robot_command = 'c'+grasp_cmd+'p'+self.empty_message
        self._send(self.robot_command)
        return self.robot_command
    
    '''
    Helper function to check and parse the command string and make
        the values readable for the Robot Hand
    '''
    def _check_command_string(self, command_string:str):

        # if "c176" in command_string:
            # replace unnesserary 
        command_string = command_string.replace("\\n", "")
        command_string = command_string.replace("\n", "")
        command_string = command_string.replace("end", "")
        # command_string = command_string.replace("c176", "")
        last = command_string.find('p')
        first = command_string.find('c')
        command = command_string[first+1:last]
        # print(command)
        command_string = command_string.replace(command,"")
        command_string = command_string.replace("c", "")
        command_string = command_string.replace("p", "")
        command_string = command_string.replace("[", "")
        command_string = command_string.replace("]", "")

        #debugging
        # print(command_string)

        # seperate the two lists of joint angles and joint velocities
        command_string_position, command_string_velocity = command_string.split("v")
        # convert to list
        command_string_position = command_string_position.split(",")
        command_string_velocity = command_string_velocity.split(",")

        # debugging
        # print(command_string_velocity)

        # check the len of each element in the list
        for i in range(len(command_string_position)):
            if len(command_string_position[i]) == 1:
                command_string_position[i] = "+0" + command_string_position[i]
            elif len(command_string_position[i]) == 2 and command_string_position[i][0] != "-":
                command_string_position[i] = "+" + command_string_position[i]
            elif len(command_string_position[i]) == 2:
                command_string_position[i] = "-0" + command_string_position[i][1:]

        for i in range(len(command_string_velocity)):
            if len(command_string_velocity[i]) == 1:
                command_string_velocity[i] = "+0" + command_string_velocity[i]
            elif len(command_string_velocity[i]) == 2:
                command_string_velocity[i] = "+" + command_string_velocity[i]

        # convert back to original format
        command_string_position = "[" + ",".join(command_string_position) + "]"
        command_string_velocity = "[" + ",".join(command_string_velocity) + "]"

        # combine the two lists
        command_string = "c"+command+"p"+command_string_position + "v" + command_string_velocity + "end\n"

        return command_string