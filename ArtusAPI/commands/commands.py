
import time

class Commands:

    def __init__(self,
                 target_command = 176,
                 calibration_command = 55,
                 start_command = 88,
                 sleep_command = 25,
                 get_feedback_command = 20,
                 firmware_update_command= 52,
                 locked_reset_low_command = 12,
                 save_grasp_on_board = 200,
                 get_grasp_on_board = 210
                ):
        
        # commands 
        self.target_command = target_command
        self.calibration_command = calibration_command
        self.start_command = start_command
        self.sleep_command = sleep_command
        self.get_feedback_command = get_feedback_command
        self.firmware_update_command = firmware_update_command
        self.locked_reset_low_command = locked_reset_low_command

    def get_robot_start_command(self) -> list:
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

        return [self.start_command,20,year,month,day,hour,minute,second]


    def get_target_position_command(self) -> list:
        command_list = [0]*33 # create empty buffer
        # fill command list with data
        for name,joint_data in self.hand_joints.items():
            command_list[joint_data.index] = joint_data.target_angle
            command_list[joint_data.index+16] = joint_data.velocity
        # insert the command
        command_list.insert(0,self.target_command)
        
        return command_list

    def get_calibration_command(self):
        command_list = [0]*33
        command_list.insert(0,self.calibration_command)
        return command_list

    def get_sleep_command(self):
        command_list = [0]*33
        command_list.insert(0,self.sleep_command)
        return command_list

    def get_states_command(self):
        command_list = [0]*33
        command_list.insert(0,self.get_feedback_command)
        return command_list
    
    def get_firmware_update_command(self):
        command_list = [0]*33
        command_list.insert(0,self.firmware_update_command)
        return command_list
    
    def get_locked_reset_low_command(self, joint=None, motor=None):
        command_list = [0]*33
        command_list.insert(0,self.calibration_command)
        
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