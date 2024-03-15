import serial
import time

class UART:
    def __init__(self,
                 port='COM9',
                 baudrate=115200, #115200, 
                 timeout=0):
        
        # automatically connect to the first available port
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        # self.esp32 = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.esp32 = serial.Serial(baudrate=self.baudrate, timeout= self.timeout)

    def open(self):
        self.esp32.port=self.port
        self.esp32.close()
        self.esp32.open()

    def send(self, data):
        self.esp32.write(data.encode())
        #print(data.encode())

    def receive(self):
        ## check if something is available to read
        if self.esp32.in_waiting > 100: # receive the message and decode it to utf-8
            data = self.esp32.readline().decode()
            #print(data)
            return str(data)
        return ""

    def close(self):
        self.esp32.close()



def test_serial_receive():
    esp32_communication = UART()
    esp32_communication.start()
    while True:
        msg = esp32_communication.receive()
        if msg != "":
            print(msg)

def test_serial_send():
    esp32_communication = UART()
    esp32_communication.start()
    while True:
        esp32_communication.send("hello\n")
        time.sleep(1)


if __name__ == "__main__":
    test_serial_receive()
    # test_serial_send()