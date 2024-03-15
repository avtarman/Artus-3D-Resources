
import sys
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent
sys.path.append(str(desired_path))
print(desired_path)



from ArtusAPI.communication.communication import Communication
from ArtusAPI.commands.commands import Commands
from ArtusAPI.robot.robot import Robot
import time

class ArtusAPI:

    def __init__(self,
                #  communication
                communication_method='UART',
                communication_channel_identifier='COM9',
                #  robot
                robot_type='artus_lite',
                hand_type ='left'):

        self.communication_handler = Communication(communication_method=communication_method,
                                                  communication_channel_identifier=communication_channel_identifier)
        self.command_handler = Commands()
        self.robot_handler = Robot(robot_type = robot_type,
                                   hand_type = hand_type)
        
        self._last_command_sent_time = time.perf_counter()
        self._communication_frequency = 0.01 # 100 Hz

    
    # communication setup
    def connect(self):
        return self.communication_handler.open_connection()
    def disconnect(self):
        return self.communication_handler.close_connection()
    

    

    # robot states
    def wake_up(self):
        robot_wake_up_command = self.command_handler.get_robot_wake_up_command()
        return self.communication_handler.send(robot_wake_up_command)
    def sleep(self):
        robot_sleep_command = self.command_handler.get_robot_sleep_command()
        return self.communication_handler.send(robot_sleep_command)
    def calibrate(self):
        robot_calibrate_command = self.command_handler.get_robot_calibrate_command()
        return self.communication_handler.send(robot_calibrate_command)
    

    # robot control
    def set_joint_angles(self, joint_angles):
        joint_angles = self.robot_handler.set_joint_angles(joint_angles = joint_angles)
        robot_set_joint_angles_command = self.command_handler.get_robot_set_joint_angles_command(joint_angles = joint_angles)
        # check communication frequency
        if not self._check_communication_frequency():
            return False
        return self.communication_handler.send(robot_set_joint_angles_command)
    
    def set_home_position(self):
        hand_home_position = self.robot_handler.set_home_position()
        robot_set_home_position_command = self.command_handler.get_robot_set_joint_angles_command(hand_home_position = hand_home_position)
        # check communication frequency
        if not self._check_communication_frequency():
            return False
        return self.communication_handler.send(robot_set_home_position_command)

    def _check_communication_frequency(self):
        """
        check if the communication frequency is too high
        """
        current_time = time.perf_counter()
        if current_time - self._last_command_sent_time < self._communication_frequency:
            print("Command not sent. Communication frequency is too high.")
            return False
        self._last_command_sent_time = current_time
        return True



    # robot feedback
    def receive_feedback(self):
        feedback_command = self.command_handler.get_robot_feedback_command()
        self.communication_handler.send(feedback_command)
        return self.communication_handler.receive()
    
    def get_joint_angles(self):
        feedback_command = self.receive_feedback()
        joint_angles = self.robot_handler.get_joint_angles(feedback_command)
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