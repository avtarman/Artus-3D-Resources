
import logging
import time



import sys
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent.parent
sys.path.append(str(desired_path))
print(desired_path)

# Communication methodss
from ArtusAPI.communication.WiFi.wifi_server import WiFiServer
from ArtusAPI.communication.UART.uart import UART
# from ArtusAPI.ArtusAPI.communication.can import CAN

class Communication:
    """
    This communication class contains two communication methods:
        - UART
        - WiFi
    """
    def __init__(self,
                 communication_method='UART',
                 communication_channel_identifier='COM9'):
        # initialize communication
        self.communication_method = communication_method
        self.communication_channel_identifier = communication_channel_identifier
        self.communicator = None
        # setup communication
        self._setup_communication()

    
    ################# Communication: _Initialization ##################
    def _setup_communication(self):
        """
        Initialize communication based on the desired method; UART or WiFi
        """
        # setup communication based on the method
        if self.communication_method == 'UART':
            self.communicator = UART(port=self.communication_channel_identifier)
        elif self.communication_method == 'WiFi':
            self.communicator = WiFiServer(target_ssid=self.communication_channel_identifier)
        else:
            raise ValueError("Unknown communication method")
       
    
    ################# Communication: Public Methods ##################
    def open_connection(self):
        """
        start the communication
        """
        self.communicator.open()

    def send_data(self, message):
        """
        send message
        """
        try:
            self.communicator.send(message)
            return True
        except Exception as e:
            logging.warning("unable to send command")
            print(e)
            pass
        return False

    def receive_data(self):
        """
        receive message
        """
        try:    
            message_received = self.communicator.receive()
        except Exception as e:
            logging.warning("unable to receive message")
            print(e)
        return message_received

    def close_connection(self):
        self.communicator.close()


##################################################################
############################## TESTS #############################
##################################################################
def test_wifi():
    communication = Communication(communication_method='WiFi', communication_channel_identifier='Artus3D')
    communication.open_connection()
    while True:
        msg = communication.receive()
        if msg != "":
            print(msg)

def test_uart():
    communication = Communication(communication_method='UART', communication_channel_identifier='COM9')
    communication.open_connection()
    while True:
        communication.send("hello\n")
        time.sleep(1)


if __name__ == "__main__":
    # test_wifi()
    test_uart()



    
