import socket
import time
import os
import subprocess
import platform
import psutil
import logging

class WiFiServer:

    def __init__(self,
                 HEADER = 64,# Header size
                 FORMAT = "utf-8", # Format of the message
                 DISCONNECT_MESSAGE = "!DISCONNECT", # Disconnection message from the client
                 port= 5050,
                 target_ssid="Artus3DTester",
                 password = None, # possibility to take in password
                 logger = None):
        
        self.HEADER = HEADER
        self.FORMAT = FORMAT
        self.DISCONNECT_MESSAGE = DISCONNECT_MESSAGE
        self.password = password

        self.target_ssid = target_ssid
        ip = None
        
        # Looking for IP 192.168.4.2
        # Port Number
        self.port = port

        self.server_socket = None
        self.conn = None
        self.addr = None

        self.maximum_freq = None
        if not logger:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def _get_available_ip(self):
        gateway_ip = None
        
        # Get all network interfaces
        interfaces = psutil.net_if_addrs()

        for interface,addresses in interfaces.items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    if "192.168.4" in address.address:
                        try:
                            return address.address
                        except KeyError:
                            #TODO logging
                            self.logger.error(f"No gateway information available")
                            None

        return None

    """ Start server and listen for connections """
    def open(self):
        try:

            # look for wifi
            self._find_ssid()

            # get IP addresses associated with local machine
            source_ip = self._get_available_ip()
            # TCP tuple
            self.esp = (source_ip,self.port)

            # create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.settimeout(8) # blocking timeout to connect
            self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.server_socket.bind(self.esp)

            # listen for connections
            self.server_socket.listen()
            # TODO logging
            self.logger.info(f"Listening for connection")
        except Exception as e:
            self.logger.error(f"No Network named {self.target_ssid}")

        # Accept the connection
        try:
            self.conn, self.addr = self.server_socket.accept()
            self.conn.settimeout(0.1) # 1 ms timeout for recv and send methods
            # TODO logging
            self.logger.info(f"New Connection: {self.addr} connected.")
        except TimeoutError as e:
            self.logger.error('Connection Timeout')
            # TODO logging
        time.sleep(1)

    def _find_ssid(self):
        sys = platform.system()

        if sys == "Windows":
            # set profile location
            self.wifi_profile = os.getcwd()+self.target_ssid+".xml"

            # prompt user if first time
            if not os.path.isfile(os.getcwd()+'\\Wi-Fi-'+self.target_ssid+'.xml'):
                # wait for connecting first time
                input("First time Connection, Please connect to Artus Hand and enter Y when done")
                
                time.sleep(1)

                # save profile
                save_profile_cmd = f'netsh wlan export profile {self.target_ssid} key=clear folder={os.getcwd()}'
                subprocess.run(save_profile_cmd,shell=True)

                time.sleep(1)
                
                if not os.path.isfile(os.getcwd()+'\\Wi-Fi-'+self.target_ssid+'.xml'):
                    # TODO logging
                    self.logger.warning(f"Unable to create wifi profile")

            else:
                # connect to profile 
                connect_command = f'netsh wlan connect ssid={self.target_ssid} name={self.target_ssid} interface=Wi-Fi'
                subprocess.run(connect_command, shell=True)

        elif sys == "Linux":
            # Linux uses the "nmcli" command to connect to Wi-Fi networks
            connect_command = f'nmcli dev wifi connect "{self.target_ssid}"'

            # input password
            if not self.password:
                self.password = input('type ssid password:')
            if self.password:
                connect_command += f' password "{self.password}"'

            subprocess.run(connect_command, shell=True)
            
            # clear password
            self.password = None
        
        else:
            # TODO logging
            self.logger.error("Unsupported operating system")

        # wait X seconds to connect
        for i in range(10):
            time.sleep(0.01)

    def close(self):
        self.server_socket.close()
        system = platform.system()

        if system == "Windows":
            # Windows uses the "netsh" command to disconnect from Wi-Fi networks
            disconnect_command = f'netsh wlan disconnect interface="Wi-Fi" ssid="{self.target_ssid}"'
            subprocess.run(disconnect_command, shell=True)

        elif system == "Linux":
            # Linux uses the "nmcli" command to disconnect from Wi-Fi networks
            disconnect_command = f'nmcli dev disconnect iface "wlp2s0" ssid "{self.target_ssid}"'
            subprocess.run(disconnect_command, shell=True)

        else:
            # TODO logging
            self.logger.error("Unsupported operating system")
            return

        # TODO logging
        self.logger.info(f"Disconnected from {self.target_ssid}")
        time.sleep(2)  # Wait for a few seconds for the disconnect to take effect

        return 
    
    def receive(self):
        try:
            byte_msg = self.conn.recv(65) # receive bytes

            if len(byte_msg) == 65: # receive the first 65 bytes
                return byte_msg

            else:
                self.logger.warning(f"Incomplete data received - package size = {len(byte_msg)}")
                return None
        except Exception as e:
            # TODO logging
            self.logger.warning(f"No data available to receive")
            return None

    
    def send(self, data:bytearray):
        try:
            self.conn.sendall(data)
        except Exception as e:
            # TODO insert error logging
            self.logger.error(f"Unable to send data")
            None
 
    def flash_wifi(self): 
        acknowledged = False

        file_location = input("Enter file path: ")
        # file_location = "C:\\Users\\RyanLee\\Documents\\GitHub\\Artus-3D-actuators-fw\\Debug\\actuator_m0.bin"
        file_size = os.path.getsize(file_location) 

        self.conn.send("file ready\n".encode())
        self.conn.send((str(file_size)+"\n").encode())
        file = open(file_location, "rb")
        file_data = file.read()
        file.close
        self.conn.sendall(file_data)

        while not acknowledged:
            message = self.conn.recv(1024).decode()
            if message == "failed":
                print("File upload failed\n")
                acknowledged = True
            elif message == "success":   
                print("File upload successful\n")
                acknowledged = True

        print("Flashing...")
        
        while True:
            message = self.conn.recv(1024).decode()
            if message == "FLASHED":
                print("Firmware update complete")
                break
    
    def upload_logs_wifi():
        while True:
            # receive here
            if """ finishing condition""":
                break
        return
