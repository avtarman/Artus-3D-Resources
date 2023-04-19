
class ESP32Commands:

    def __init__(self,
                TARGET = 176,
                CALIBRATE = 55,
                SHUTDOWN = 25,
                DUMMY = 11,
                DONECOMMAND = 211,
                START = 88,
                PID = 50):
        
        self.TARGET = TARGET
        self.CALIBRATE = CALIBRATE
        self.SHUTDOWN = SHUTDOWN
        self.DUMMY = DUMMY
        self.DONECOMMAND = DONECOMMAND
        self.START = START
        self.PID = PID
        self.user_input = None

        self.twosend = [0] * 16 # will always send an array of size 16
        self.array_start_value = 200
        self.twosend[0] = self.array_start_value

        self.kvals = ['kp','kd','ki']

    def get_command(self):
        return self.twosend
    """ 
        Handle keyboard input to send commands to ESP32 
        @returns -> cmd array and flag boolean for whether needs a return signal or not
    """
    def set_command_userInput(self):
        self.user_input = input("[INPUT] Waiting for command...\n[OPTIONS]\n[t]\tTarget\n[c]\tCalibrate\n[st]\tStart\n[p]\tPID\n")
        # easy to add more options here
        self.twosend[0] = 200
        #### start command ####
        if self.user_input == 'st':
            self.twosend[1] = self.START
        #### calibrate command ####
        elif self.user_input == 'c':
            self.twosend[1] = self.CALIBRATE
        #### setting PID command ####
        elif self.user_input == 'p':
            self.twosend[1] = self.PID
            ## set the PID values
            self._set_pid_values()
        #### tagetting command ####
        elif self.user_input == 't':
            return True # return true because we want a return signal
        else:
            return False # return false because we don't care about a return signal
        return True # return true because we want a return signal
    
    def _set_pid_values(self):
        self.user_input = input('[INPUT] [1-8] choose STM to change: ')
        self.twosend[2] = self.user_input
        # 3=kp 4=kd 5=ki
        for i,k in enumerate(self.kvals):
            self.user_input = input('[INPUT] Please enter (to 1 decimal point) '+k+' value: ')
            self.twosend[3+i] = self.user_input


def main():
    commands = ESP32Commands()
    while True:
        commands.set_command_userInput()
        print(commands.get_command())

if __name__ == "__main__":
    main()

