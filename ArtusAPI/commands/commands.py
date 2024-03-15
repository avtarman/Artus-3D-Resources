
class Commands:

    def __init__(self,
                 target_command = "176",
                 calibration_command = "55",
                 start_command = "88",
                 sleep_command = "25",
                 get_states_command = "10",
                 firmware_update_command= "52",
                 locked_reset_low_command = "12"
                ):
        
        self.target_command = target_command
        self.calibration_command = calibration_command
        self.start_command = start_command
        self.sleep_command = sleep_command
        self.get_states_command = get_states_command
        self.firmware_update_command = firmware_update_command
        self.locked_reset_low_command = locked_reset_low_command


        self.generic_commmad_message_structure = "p[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]" \
                                                "v[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]end\n"

    def get_robot_start_command(self):
        """
        Creates a message to start the hand
        """

        command = self.start_command

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

        message_string = 'c{command},' \
                        'p[20,{year},+{month},+{day},+{hour},+{minute},+{second},00,00,00,00,00,00,00,00,00]' \
                        'v[00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]end\n'.format(command=command,
                                                                                              year=year,
                                                                                              month=month,
                                                                                              day=day,
                                                                                              hour=hour,
                                                                                              minute=minute,
                                                                                              second=second)
                                                                                                                                                                              
        return message_string


    def get_target_position_command(self, positions=None, velocities=None):
        command = self.target_command
        message_string = 'c{0}p[{1}]v[{2}]end\n'.format(
            command,
            ','.join(str(position) for position in positions),
            ','.join(str(velocity) for velocity in velocities)
        )
        return message_string

    def get_calibration_command(self):
        calibration_command = self.calibration_command
        return "c{calibration_command}".format(calibration_command=calibration_command) + self.generic_commmad_message_structure

    def get_sleep_command(self):
        sleep_command = self.sleep_command
        return "c{sleep_command}".format(sleep_command=sleep_command) + self.generic_commmad_message_structure

    def get_states_command(self):
        get_states_command = self.get_states_command
        return "c{get_states_command}".format(get_states_command=get_states_command) + self.generic_commmad_message_structure

    def get_firmware_update_command(self):
        firmware_update_command = self.firmware_update_command
        return "c{firmware_update_command}".format(firmware_update_command=firmware_update_command) + self.generic_commmad_message_structure
    
    def get_locked_reset_low_command(self, joint=None, act=None):
        locked_reset_low_command = self.locked_reset_low_command
        return "c{locked_reset_low_command}p[{joint},0{act},00,00,00,00,00,00,00,00,00,00,00,00,00,00,00]v[00".format(locked_reset_low_command=locked_reset_low_command,
                                                                                                                        joint=joint,
                                                                                                                        act=act)
        
    # def _build_command(self, command_message, position=None, velocity=None):
    #     if position is not None and velocity is not None:
    #         command = "c{0}".format(command_message) + self.generic_commmad_message_structure
    #         return command_message + '*' + self._command_checksum(command_message) + '\n'
    #     else:
    #         return command_message + '*' + self._command_checksum(command_message) + '\n'


def test_command_builder():
    command_builder = CommandBuilder()
    print(command_builder.get_robot_start_command())


if __name__ == "__main__":
    test_command_builder()