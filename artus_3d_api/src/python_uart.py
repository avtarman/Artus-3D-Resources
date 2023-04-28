import serial
import time

class PythonEsp32Serial:

    def __init__(self, port='COM3', baudrate=115200, timeout=5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        # self.esp32 = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.esp32 = serial.Serial(baudrate=self.baudrate, timeout=self.timeout)

    def start(self):
        self.esp32.port=self.port
        self.esp32.close()
        self.esp32.open()

    def send(self, data):
        self.esp32.write(data.encode())

    def recieve(self):
        data = self.esp32.readline()
        return data
        
    def close(self):
        self.esp32.close()