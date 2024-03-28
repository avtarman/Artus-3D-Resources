
import sys
import logging
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent
sys.path.append(str(desired_path))
print(desired_path)



from .communication import Communication
from .commands import Commands
from .robot import Robot
import time

class ArtusAPI:

    def __init__(self,
                #  communication
                communication_method='UART',
                communication_channel_identifier='COM9',
                #  robot
                robot_type='artus_lite',
                hand_type ='left',
                stream = False,
                communication_frequency = 400, # hz
                logger = None
                ):

        self._communication_handler = Communication(communication_method=communication_method,
                                                  communication_channel_identifier=communication_channel_identifier)
        self._command_handler = Commands()
        self._robot_handler = Robot(robot_type = robot_type,
                                   hand_type = hand_type)
        
        self._last_command_sent_time = time.perf_counter()
        self._communication_frequency = 1 / communication_frequency
        self._communication_frequency_us = int(self._communication_frequency * 1000000)
        self.stream = stream

        if not logger:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
    
    # communication setup
    def connect(self):
        return self._communication_handler.open_connection()
    def disconnect(self):
        return self._communication_handler.close_connection()
    

    

    # robot states
    def wake_up(self):
        print(f"communication frequency in useconds = {self._communication_frequency_us}")
        robot_wake_up_command = self._command_handler.get_robot_start_command(self.stream,self._communication_frequency_us) # to ms for masterboard
        return self._communication_handler.send_data(robot_wake_up_command)
    def sleep(self):
        robot_sleep_command = self._command_handler.get_sleep_command()
        return self._communication_handler.send_data(robot_sleep_command)
    def calibrate(self):
        robot_calibrate_command = self._command_handler.get_calibration_command()
        return self._communication_handler.send_data(robot_calibrate_command)
    

    # robot control
    def set_joint_angles(self, joint_angles:dict):
        self._robot_handler.set_joint_angles(joint_angles=joint_angles,name=False)
        robot_set_joint_angles_command = self._command_handler.get_target_position_command(self._robot_handler.robot.hand_joints)
        # check communication frequency
        if not self._check_communication_frequency():
            return False
        return self._communication_handler.send_data(robot_set_joint_angles_command)
    
    def set_home_position(self):
        self._robot_handler.set_home_position()
        robot_set_home_position_command = self._command_handler.get_target_position_command()
        # check communication frequency
        if not self._check_communication_frequency():
            return False
        return self._communication_handler.send_data(robot_set_home_position_command)

    def _check_communication_frequency(self):
        """
        check if the communication frequency is too high
        """
        current_time = time.perf_counter()
        if current_time - self._last_command_sent_time < self._communication_frequency:
            self.logger.warning("Command not sent. Communication frequency is too high.")
            return False
        self._last_command_sent_time = current_time
        return True



    # robot feedback
    def _receive_feedback(self):
        feedback_command = self._command_handler.get_states_command()
        self._communication_handler.send_data(feedback_command)
        return self._communication_handler.receive_data()
    
    def get_joint_angles(self):
        feedback_command = self._receive_feedback()
        joint_angles = self._robot_handler.get_joint_angles(feedback_command)
        return joint_angles
    
    # robot feedback stream
    def get_streamed_joint_angles(self):
        if not self._check_communication_frequency():
            return False
        feedback_command = self._communication_handler.receive_data()
        if not feedback_command:
            return None
        joint_angles = self._robot_handler.get_joint_angles(feedback_command)
        return joint_angles

        
    


def test_artus_api():
    artus_api = ArtusAPI()
    artus_api.connect()
    artus_api.wake_up()
    artus_api.calibrate()
    artus_api.set_home_position()
    time.sleep(2)
    artus_api.disconnect()

if __name__ == "__main__":
    test_artus_api()