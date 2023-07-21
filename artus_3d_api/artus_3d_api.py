
import time
import numpy as np
import ast

import os
current_directory = os.getcwd()
# print(current_directory)
# src_directory = os.path.join(current_directory, "src")
import sys
sys.path.append(current_directory)
from src.python_server import PythonServer
from src.python_uart import PythonEsp32Serial

class Artus3DAPI:

    def __init__(self,
                communication_method = "WiFi", # wifi or uart (default: wifi)
                port='COM9'):


        self.command_filename = "command.txt"
        self.communication_method = communication_method
        self.port = port

        self.command = 0 # command for robot for calibration, target control, etc.
        self.default_velocity = 70 # default velocity for velocity control
        self.joint_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.joint_velocities = [70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70]
        self.joint_accelerations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.robot_command = {'joint_angles': self.joint_angles,
                              'joint_velocities': self.joint_velocities,
                              'joint_accelerations': self.joint_accelerations}
        
        self.grasp_patterns = None
        
        self.python_server = PythonServer(reqReturnFlag = False)
      
        self.python_serial = PythonEsp32Serial(port=self.port)

        if self.communication_method == "WiFi":
            self.python_server.start()

        if self.communication_method == "UART":
            try:
                self.python_serial.start()
                ## clear buffer
                for i in range(10):
                    self.python_serial.receive()
            except Exception as e:
                print("UART not connected")
                print(e)
                pass

    def set_joint_angles(self, joint_angles):
        self.joint_angles = joint_angles

    def set_joint_velocities(self, joint_velocity):
        self.joint_velocities = joint_velocity

    def set_joint_accelerations(self, joint_acceleration):
        self.joint_accelerations = joint_acceleration

    def get_robot_states(self):
        """
        Get Robot States
        """
        # Get Robot States based on communication method
        states = ""

        robot_states_command = "c10p[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"

        self.send (robot_states_command)
        states  = ""
        while "position" not in states:
            states  = self.receive()
        return states
    
    def get_debug_message(self):
        """
        Get Debug Message
        """
        # Get Debug Message based on communication method
        debug_command = "c11p[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        self.send(debug_command)
        debug_message = ""
        while "debug" not in debug_message:
            debug_message  = self.receive()
        return debug_message
    
    def save_current_positions(self):
        # get states back
        states = self.get_robot_states()
        states = self.get_robot_states()

        # find substring
        startInd = states.find("[")
        endInd = states.find("]",startInd)

        lastpositions = states[startInd:endInd]

        # make a directory for saving positions
        if not os.path.exists("pos"):
            os.makedirs("pos")
        # save last positions before shutdown
        np.save("pos/lastpositions",lastpositions)

    def start(self):
        """
        Shut down the robot
        """
        self.robot_command = "c88p[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        # send command
        self.send(self.robot_command)

    def reset_low(self,joint:str,act:str):
        """
        send joint back to 0
        """
        if int(joint) < 10:
            joint = '0'+joint
        self.robot_command = "c12p["+joint+",0"+act+",00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        # send command
        self.send(self.robot_command)
    
    def calibrate(self):
        """
        Calibrate Robot
        callibrate command: "calibrate"
        """
        self.robot_command = "c55p[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n"
        # send command
        self.send(self.robot_command)

        # while True:
        #     states = self.get_robot_states()
        #     print(states)
        #     if "1" in states:
        #         print("Robot Calibrated")
        #         time.sleep(2)
        #         return
        #     else:
        #         print("Calibrating Robot...")
        #         time.sleep(2)

    def save_grasp_pattern(self, 
                           name=None, 
                           grasp_pattern=None):
        """
        Save Grasp Pattern
        save grasp pattern command: "save_grasp_pattern"
        """
        if grasp_pattern is None:
            print("No Grasp Pattern")
            return  
        if name is None:
            name = input("Enter Grasp Pattern Name: ")

        # make a directory for saving grasp patterns
        if not os.path.exists("grasp_patterns"):
            os.makedirs("grasp_patterns")
        # save grasp pattern
        np.save("grasp_patterns/" + name, grasp_pattern)

        self.grasp_patterns = self._load_grasp_patterns()

    def get_grasp_command(self,
                            name=None):
        
        if name is None:
            name = input("Enter Grasp Pattern Name: ")

        if self.grasp_patterns is None:
            self.grasp_patterns = self._load_grasp_patterns()
        
        # get grasp pattern
        grasp_pattern = self.grasp_patterns[name+".npy"]
        return grasp_pattern
    
    def _load_grasp_patterns(self):
        """
        Load Grasp Patterns as Dictionary
        """

        # get all grasp patterns
        grasp_patterns = os.listdir("grasp_patterns")

        # load all grasp patterns
        self.grasp_patterns = {}
        for i in range(len(grasp_patterns)):
            self.grasp_patterns[grasp_patterns[i]] = np.load("grasp_patterns/" + grasp_patterns[i])

        return self.grasp_patterns


    def change_communication_method(self, communication_method, port=None):
        ## parse to appropriate communication method command format

        if self.communication_method == "WiFi" and communication_method == "UART":
            self.send("UART") ## send command to robot to change communication method on its side
            self.python_server.close() ## close wifi connection
            self.python_serial.start() ## open uart connection
            self.communication_method = "UART" ## update communication method

        elif self.communication_method == "UART" and communication_method == "WiFi":
            self.send("WiFi") ## send command to robot to change communication method on its side
            self.python_serial.close() ## close uart connection
            if port is not None:
                self.python_server.port = port
            self.python_server.start() ## open wifi connection
            self.communication_method = "WiFi" ## update communication method

        else:
            print("Communication Method is already ", communication_method)

    def send(self, message):
        # Send Command to Robot based on communication method
        if self.communication_method == "WiFi": # wifi

            message = self._check_command_string(message)
            print(message)
            # return
            self.python_server.send(message)
        elif self.communication_method == "UART": # uart
            self.python_serial.send(message)

    def receive(self):
        """
        Recieve Command from Robot
        """
        if self.communication_method == "WiFi": # wifi
            message  = self.python_server.receive()

        elif self.communication_method == "UART": # uart
            message  = self.python_serial.receive()

        return message


    def _parse_command(self):
                    
        """
        Parse Robot Command

        formate of command:
        "c0p[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]v[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]a[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]end"
        """

        # parse command


        self.robot_command = "c{0}p{1}v{2}a{3}end\n".format(self.command,
                                                       self.joint_angles,
                                                       self.joint_velocities,
                                                       self.joint_accelerations)
        
        return self.robot_command
    

    def _check_command_string(self, command_string):

        if "c176" in command_string:
            print(command_string)
            # replace unnesserary 
            command_string = command_string.replace("end\\n\n", "")
            command_string = command_string.replace("c176", "")
            command_string = command_string.replace("p", "")
            command_string = command_string.replace("[", "")
            command_string = command_string.replace("]", "")

            #debugging
            print(command_string)

            # seperate the two lists of joint angles and joint velocities
            command_string_position, command_string_velocity = command_string.split("v")
            # convert to list
            command_string_position = command_string_position.split(",")
            command_string_velocity = command_string_velocity.split(",")

            # debugging
            print(command_string_velocity)

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
                    command_string_velocity[i] = "00" + command_string_velocity[i]
                elif len(command_string_velocity[i]) == 2:
                    command_string_velocity[i] = "0" + command_string_velocity[i]

            # convert back to original format
            command_string_position = "[" + ",".join(command_string_position) + "]"
            command_string_velocity = "[" + ",".join(command_string_velocity) + "]"

            # combine the two lists
            command_string = "c176p"+command_string_position + "v" + command_string_velocity + "end\n"

        return command_string
