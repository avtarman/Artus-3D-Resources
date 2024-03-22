
import time
import json
import sys
import os
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent
sys.path.append(str(desired_path))
print(desired_path)

class Commands:

    def __init__(self):
        
        # commands 
        with open(os.path.join(desired_path,'commands',"commands.json")) as file:
            self.commands = json.load(file)

    def get_robot_start_command(self,stream:bool,freq:int) -> list:
        """
        Creates a message to start the hand
        """
        # RTC start time from PC
        year    = int(time.localtime().tm_year - 2000)
        month   = int(time.localtime().tm_mon)
        day     = int(time.localtime().tm_mday)
        hour    = int(time.localtime().tm_hour)
        minute  = int(time.localtime().tm_min)
        second  = int(time.localtime().tm_sec)

        if stream: 
            return [self.commands['start_command'],20,year,month,day,hour,minute,second,1,(freq>>16)&0xff,(freq>>8)&0xff,freq&0xff]
        else:
            return [self.commands['start_command'],20,year,month,day,hour,minute,second]


    def get_target_position_command(self,hand_joints:dict) -> list:
        command_list = [0]*32 # create empty buffer
        # fill command list with data
        for name,joint_data in hand_joints.items():
            command_list[joint_data.index] = joint_data.target_angle
            command_list[joint_data.index+16] = joint_data.velocity
        # insert the command
        command_list.insert(0,self.commands['target_command'])
        
        return command_list

    def get_calibration_command(self):
        command_list = [0]*32
        command_list.insert(0,self.commands['calibration_command'])
        return command_list

    def get_sleep_command(self):
        command_list = [0]*32
        command_list.insert(0,self.commands['sleep_command'])
        return command_list

    def get_states_command(self):
        command_list = [0]*32
        command_list.insert(0,self.commands['get_feedback_command'])
        return command_list
    
    def get_firmware_update_command(self):
        command_list = [0]*32
        command_list.insert(0,self.commands['firmware_update_command'])
        return command_list
    
    def get_locked_reset_low_command(self, joint=None, motor=None):
        command_list = [0]*32
        command_list.insert(0,self.commands['reset_command'])
        
        # constraint checker 
        if 0 <= joint <= 15:
            command_list[0] = joint
        else:
            # TODO logging
            None
        if 0 <= motor <= 2:
            command_list[1] = motor
        else:
            # TODO logging
            None
            
        return command_list


if __name__ == "__main__":
    None