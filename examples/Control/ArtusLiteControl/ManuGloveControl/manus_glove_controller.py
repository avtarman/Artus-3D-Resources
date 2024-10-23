import time
import numpy as np


import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
print("Project Root", PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)
from Isaac_Sim_Work.Control.configuration.configuration import ArtusLiteConfig
from Isaac_Sim_Work.Control.ArtusLiteControl.ArtusLiteJointStreamer.artusLite_jointStreamer import ArtusLiteJointStreamer
from Isaac_Sim_Work.Tracking.hand_tracking.hand_tracking_data import HandTrackingData
        
class ManusGloveController:
    def __init__(self):
        """
        Update the configuration file before running the controller
        """

        # Load robot configuration
        self.robot_config = ArtusLiteConfig()
        self.artusLite_jointStreamers = {'left': None, 'right': None}
        self._initialize_api()

        # Hand Tracker
        self.hand_tracking_data = HandTrackingData(hand_tracking_method='manus_gloves', #'manus_gloves' 'gui'
                                                    port=65432)
        
        # run manus executable
        self._run_manus_executable()

    def _run_manus_executable(self):
        # Start Manus executable to receive data
        os.startfile(r"C:\Users\yizho\Documents\Sarcomere\MANUS\MANUS_Core_2.3.0.1_SDK\MANUS_Core_2.3.0.1_SDK\ManusSDK_v2.3.0.1\SDKClient\Output\x64\Debug\Client\SDKClient.exe")
        time.sleep(5)


    def _initialize_api(self):
        # Check and print configuration for left hand robot
        if self.robot_config.config.robots.left_hand_robot.robot_connected:
            self.artusLite_jointStreamers['left'] = ArtusLiteJointStreamer(communication_method=self.robot_config.config.robots.left_hand_robot.communication_method,
                                                                            communication_channel_identifier=self.robot_config.config.robots.left_hand_robot.communication_channel_identifier,
                                                                            hand_type='left',
                                                                            reset_on_start=self.robot_config.config.robots.left_hand_robot.reset_on_start,
                                                                            streaming_frequency=self.robot_config.config.robots.left_hand_robot.streaming_frequency,
                                                                            start_robot=self.robot_config.config.robots.left_hand_robot.start_robot,
                                                                            calibrate=self.robot_config.config.robots.left_hand_robot.calibrate,
                                                                            robot_connected=self.robot_config.config.robots.left_hand_robot.robot_connected)
            
        # Check and print configuration for right hand robot
        if self.robot_config.config.robots.right_hand_robot.robot_connected:
            self.artusLite_jointStreamers['right'] = ArtusLiteJointStreamer(communication_method=self.robot_config.config.robots.right_hand_robot.communication_method,
                                                                            communication_channel_identifier=self.robot_config.config.robots.right_hand_robot.communication_channel_identifier,
                                                                            hand_type='right',
                                                                            reset_on_start=self.robot_config.config.robots.right_hand_robot.reset_on_start,
                                                                            streaming_frequency=self.robot_config.config.robots.right_hand_robot.streaming_frequency,
                                                                            start_robot=self.robot_config.config.robots.right_hand_robot.start_robot,
                                                                            calibrate=self.robot_config.config.robots.right_hand_robot.calibrate,
                                                                            robot_connected=self.robot_config.config.robots.right_hand_robot.robot_connected)

    def start_streaming(self):
        while True:
            try:
                # Get joint angles from the hand
                for i in range(5):
                    joint_angles_left, joint_angles_right  = self.hand_tracking_data.get_finger_joint_rotations_list_rad(hand="LR")
                
                # Left hand
                print("Joint Angles Left: ",joint_angles_left)
                # map joint positions from isaac sim to robot hand
                current_joint_left = self._manus_to_robot_joint_mapper_L(joint_angles=joint_angles_left.copy())

                # Right hand
                print("Joint Angles Right: ",joint_angles_right)
                # map joint positions from isaac sim to robot hand
                current_joint_right = self._manus_to_robot_joint_mapper_R(joint_angles=joint_angles_right.copy())

                # Stream joint angles to the hands
                self._send_joint_angles(joint_angles_left=current_joint_left, joint_angles_right=current_joint_right)

            except Exception as e:
                print(e)
                pass

    def _send_joint_angles(self, joint_angles_left=None, joint_angles_right=None):
        if self.artusLite_jointStreamers['left'] is not None:
            self.artusLite_jointStreamers['left'].stream_joint_angles(joint_angles=joint_angles_left)
        if self.artusLite_jointStreamers['right'] is not None:
            self.artusLite_jointStreamers['right'].stream_joint_angles(joint_angles=joint_angles_right)


    def _manus_to_robot_joint_mapper_L(joint_angles = None):

        robot_joint_angles = []
        if joint_angles is not None:

            robot_joint_angles = [-joint_angles[4],joint_angles[9],joint_angles[14], joint_angles[19], # thumb
                                -joint_angles[0], joint_angles[5], joint_angles[10], # index
                                -joint_angles[1], joint_angles[6], joint_angles[11], # middle
                                -joint_angles[3], joint_angles[8], joint_angles[13], # ring
                                -joint_angles[2], joint_angles[7], joint_angles[12]] # pinky
            # make sure all intsq
            # robot_joint_angles = [int(i) for i in robot_joint_angles]


            robot_joint_angles = np.rad2deg(robot_joint_angles) 
            print("SENDING Joint angles                                                            ************",  robot_joint_angles)
        return robot_joint_angles

    def _manus_to_robot_joint_mapper_R(joint_angles = None):

        robot_joint_angles = []
        if joint_angles is not None:

            robot_joint_angles = [joint_angles[4],joint_angles[9],joint_angles[14], joint_angles[19], # thumb
                                joint_angles[0], joint_angles[5], joint_angles[10], # index
                                joint_angles[1], joint_angles[6], joint_angles[11], # middle
                                joint_angles[3], joint_angles[8], joint_angles[13], # ring
                                joint_angles[2], joint_angles[7], joint_angles[12]] # pinky
            # make sure all ints
            # robot_joint_angles = [int(i) for i in robot_joint_angles]


            robot_joint_angles = np.rad2deg(robot_joint_angles) 
            print("SENDING Joint angles                                                            ************",  robot_joint_angles)
        return robot_joint_angles
    


def both_hands_control_manus_gloves():
    manus_glove_joint_angles_streamer = ManusGloveController()
    manus_glove_joint_angles_streamer.start_streaming()


if __name__ == '__main__':
    both_hands_control_manus_gloves()

# "C:\Users\General User\AppData\Local\ov\pkg\isaac_sim-2022.2.1\python.bat" "c:/Users/General User/Desktop/github_files/Isaac_Sim_Work/Hand_Simulation/handTracking_simulation_robotControl/artus3d_joint_angles_streamer/joint_angles_streamer.py"