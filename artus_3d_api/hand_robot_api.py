
import time

import os
current_directory = os.getcwd()
# print(current_directory)
# src_directory = os.path.join(current_directory, "src")
import sys
sys.path.append(current_directory)
from src.python_server import PythonServer
from src.esp32_commands import ESP32Commands

class HandRobotAPI:

    def __init__(self, robot_id="1234567", robot_password="abcd"):
        self.robot_id = robot_id
        self.robot_password = robot_password
        self.command_filename = "command.txt"

        self.joint_angles = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.joint_velocities = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.joint_accelerations = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.robot_command = {'joint_angles': self.joint_angles,
                              'joint_velocities': self.joint_velocities,
                              'joint_accelerations': self.joint_accelerations}
        
        self.python_server = PythonServer(reqReturnFlag = False)
        self.python_server.start()
        self.esp32_command = ESP32Commands()

    def set_joint_angles(self, joint_angles):
        self.joint_angles = joint_angles

    def set_joint_velocity(self, joint_velocity):
        self.joint_velocities = joint_velocity

    def set_joint_acceleration(self, joint_acceleration):
        self.joint_accelerations = joint_acceleration

    def visualize(self):
        """
        TODO: Run Simulation
        """
        pass

    def send_command(self):
        """
        Send Command to Robot

        Format:
        self.robot_command = {
                                'joint_angles': self.joint_angles, 
                                'joint_velocities': self.joint_velocities,
                                'joint_accelerations': self.joint_accelerations
                             }
        """
        self.robot_command = {'joint_angles': self.joint_angles,
                'joint_velocities': self.joint_velocities,
                'joint_accelerations': self.joint_accelerations}
        
        # Send Command to Robot
        self.python_server.send(self.robot_command)

    def teleoperation_mode(self,
                        joint_angles=None,
                        joint_velocities='default',
                        joint_accelerations='default'):
        
        """
        Teleoperation Mode:
        1. Set fixed values for joint velocities and joint accelerations (or use default values)
        2. Set joint angles
        """

        #  setting joint angles
        self.joint_angles = joint_angles

        # setting joint velocities
        if joint_velocities == 'default':
            pass
        else:
            self.joint_velocities = joint_velocities

        # setting joint accelerations
        if joint_accelerations == 'default':
            pass
        else:
            self.joint_accelerations = joint_accelerations
            
        # Send Command to Robot
        self.robot_command = {'joint_angles': self.joint_angles,
                'joint_velocities': self.joint_velocities,
                'joint_accelerations': self.joint_accelerations}
        
        self.python_server.send(self.robot_command)


        
    def get_robot_states(self):
        """
        Get Robot States
        """
        # self.python_server.get_states 
        position = None
        force = None
        temperature = None

        states = {'Position': position, 'Force': force, 'Temperature': temperature}
        return states