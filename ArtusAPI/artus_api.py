
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
from .firmware_update import FirmwareUpdater
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
                logger = None,
                reset_on_start = 0,
                baudrate = 921600
                ):
        """
        ArtusAPI class controls the communication and control of between a system and an Artus Hand by Sarcomere Dynamics Inc.
        :communication_method: communication method that is supported on the Artus Hand
        :communication_channel_identifier: channel identifier for the communication method
        :robot_type: name of the series of robot hand
        :hand_type: left or right
        :stream: streaming feedback data
        :communication_frequency: maximum frequency to stream data
        :logger: python logger settings to inherit
        """

        self._communication_handler = Communication(communication_method=communication_method,
                                                  communication_channel_identifier=communication_channel_identifier,baudrate=baudrate)
        self._command_handler = Commands(reset_on_start=reset_on_start)
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
        """
        Open a connection to the Artus Hand
        """
        return self._communication_handler.open_connection()
    def disconnect(self):
        """
        Close a connection to the Artus Hand
        """
        return self._communication_handler.close_connection()
    

    

    # robot states
    def wake_up(self):
        """
        Wake-up the Artus Hand
        """
        print(f"communication frequency in useconds = {self._communication_frequency_us}")
        robot_wake_up_command = self._command_handler.get_robot_start_command(self.stream,self._communication_frequency_us) # to ms for masterboard
        self._communication_handler.send_data(robot_wake_up_command)

        # wait for data back
        if self._communication_handler.wait_for_ack():
            self.logger.info(f'Finished calibration')
        else:
            self.logger.warn(f'Error in calibration')

    def sleep(self):
        """
        Sleep the Artus Hand
        """
        robot_sleep_command = self._command_handler.get_sleep_command()
        return self._communication_handler.send_data(robot_sleep_command)
    def calibrate(self):
        """
        Calibrate the Artus Hand
        """
        robot_calibrate_command = self._command_handler.get_calibration_command()
        self._communication_handler.send_data(robot_calibrate_command)

        # wait for data back
        if self._communication_handler.wait_for_ack():
            self.logger.info(f'Finished calibration')
        else:
            self.logger.warn(f'Error in calibration')
    

    # robot control
    def set_joint_angles(self, joint_angles:dict):
        """
        Set joint angle targets and speed values to the Artus Hand
        :joint_angles: dictionary of input angles and input speeds
        """
        self._robot_handler.set_joint_angles(joint_angles=joint_angles,name=False)
        robot_set_joint_angles_command = self._command_handler.get_target_position_command(self._robot_handler.robot.hand_joints)
        # check communication frequency
        if not self._check_communication_frequency():
            return False
        return self._communication_handler.send_data(robot_set_joint_angles_command)
    
    def set_home_position(self):
        """
        sends the joints to home positions (0) which opens the Artus Hand
        """
        self._robot_handler.set_home_position()
        robot_set_home_position_command = self._command_handler.get_target_position_command(hand_joints=self._robot_handler.robot.hand_joints)
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
        # test
        time.sleep(0.005)
        return self._communication_handler.receive_data()
    
    def get_joint_angles(self):
        """
        Populate feedback fields in self._robot_handler.hand_joints dict
        """
        feedback_command = self._receive_feedback()
        joint_angles = self._robot_handler.get_joint_angles(feedback_command)
        print(joint_angles)
        return joint_angles
    
    # robot feedback stream
    def get_streamed_joint_angles(self):
        """
        Populate feedback fields in self._robot_handler.hand_joints dict
        """
        if not self._check_communication_frequency():
            return False
        feedback_command = self._communication_handler.receive_data()
        if not feedback_command:
            return None
        joint_angles = self._robot_handler.get_joint_angles(feedback_command)
        return joint_angles

    def update_firmware(self):
        file_path = None
        fw_size  = 0
        # input to upload a new file
        upload_flag = input(f'Uploading a new BIN file? (y/n)  :  ')
        upload = True
            

        self._firmware_updater = FirmwareUpdater(self._communication_handler,
                                        self._command_handler)
        
        if upload_flag == 'n' or upload_flag == 'N':
            self._firmware_updater.file_location = 'not empty'
            upload = False
        else:

            self._firmware_updater.file_location = input('Please enter binfile absolute path:  ')

            fw_size = self._firmware_updater.get_bin_file_info()
        
        # set which drivers to flash should be 1-8
        drivers_to_flash = int(input(f'Which drivers would you like to flash? \n0:ALL\nor 1-8\n:  '))
        if not drivers_to_flash:
            drivers_to_flash = 0

        firmware_command = self._command_handler.get_firmware_command(fw_size,upload,drivers_to_flash)
        self._communication_handler.send_data(firmware_command)
        if upload:
            self._firmware_updater.update_firmware(fw_size)

        print(f'File size = {fw_size}')        
        print(f'flashing...')
        self._communication_handler.wait_for_ack()
        print(f'Power Cycle the device to take effect')

    def reset(self):
        j = int(input(f'Enter Joint to reset: '))
        m = int(input(f'Enter Motor to reset: '))
        reset_command = self._command_handler.get_locked_reset_low_command(j,m)
        self._communication_handler.send_data(reset_command)
    
    def hard_close(self):
        j = int(input(f'Enter Joint to reset: '))
        m = int(input(f'Enter Motor to reset: '))
        hard_close = self._command_handler.get_hard_close_command(j,m)
        self._communication_handler.send_data(hard_close)

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