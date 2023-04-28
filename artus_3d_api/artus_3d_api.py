
import time
import numpy as np

import os
current_directory = os.getcwd()
import sys
sys.path.append(current_directory)
from src.python_server import PythonServer
from src.python_uart import PythonEsp32Serial

class Artus3DAPI:

    def __init__(self,
                 communication_method = "WiFi"): # wifi or uart (default: wifi)

        self.command_filename = "command.txt"
        self.communication_method = communication_method

        self.command = 0
        self.joint_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.joint_velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.joint_accelerations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.robot_command = {'joint_angles': self.joint_angles,
                              'joint_velocities': self.joint_velocities,
                              'joint_accelerations': self.joint_accelerations}
        
        self.grasp_patterns = None
        
        self.python_server = PythonServer(reqReturnFlag = False)

        if self.communication_method == "WiFi":
            self.python_server.start()

        if self.communication_method == "UART":
            try:
                self.python_serial = PythonEsp32Serial()
                self.python_serial.start()
            except:
                print("UART not connected")
                pass

    def set_joint_angles(self, joint_angles):
        self.joint_angles = joint_angles

    def set_joint_velocities(self, joint_velocity):
        self.joint_velocities = joint_velocity

    def set_joint_accelerations(self, joint_acceleration):
        self.joint_accelerations = joint_acceleration

    def send(self, robot_command = None):
        """
        Send Command to Robot

        Format:
        self.robot_command = {
                                'joint_angles': self.joint_angles, 
                                'joint_velocities': self.joint_velocities,
                                'joint_accelerations': self.joint_accelerations
                             }
        """
        self.robot_command = self._parse_command()

        # Send Command to Robot based on communication method
        if self.communication_method == "WiFi": # wifi
            self.python_server.send(self.robot_command)

        elif self.communication_method == "UART": # uart
            self.python_serial.send(self.robot_command)

    def recieve(self):
        """
        Recieve Command from Robot
        """
        if self.communication_method == "WiFi": # wifi
            message  = self.python_server.recieve()

        elif self.communication_method == "UART": # uart
            message  = self.python_serial.recieve()

        return message

    def get_robot_states(self):
        """
        Get Robot States
        """

        # Get Robot States based on communication method
        states  = self.recieve()

        # states = {'Position': position, 'Force': force, 'Temperature': temperature}
        return states
    

    def shut_down(self):
        """
        Shut down the robot
        """
        self.command = 255 # command for shut down the robot
        self.positions = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.accelerations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # parse command
        self.robot_command = self._parse_command()

        # send command
        self.send(self.robot_command)

    
    def calibrate(self):
        """
        Calibrate Robot
        callibrate command: "calibrate"
        """
        # make calibrate command
        self.command = 55 # command for calibrate mode on the robot
        self.positions = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.accelerations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # parse command
        self.robot_command = self._parse_command()

        # send command
        self.send(self.robot_command)

        while True:
            states = self.get_robot_states()
            if states['Command'][0] == 1:
                print("Robot Calibrated")
                time.sleep(2)
                return
            else:
                print("Calibrating Robot...")
                time.sleep(2)

    def save_grasp_patter(self):
        """
        Save Grasp Pattern
        save grasp pattern command: "save_grasp_pattern"
        """
        # make save grasp pattern command
        self.command = 176 # command for targetting mode on the robot
        self.positions = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.accelerations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # parse command
        self.robot_command = self._parse_command()

        # name of grasp pattern
        self.grasp_pattern_name = input("Enter Grasp Pattern Name: ")

        # make a directory for saving grasp patterns
        if not os.path.exists("grasp_patterns"):
            os.makedirs("grasp_patterns")

        # save grasp pattern
        np.save("grasp_patterns/" + self.grasp_pattern_name, self.robot_command)
    
    def load_grasp_patterns(self):
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