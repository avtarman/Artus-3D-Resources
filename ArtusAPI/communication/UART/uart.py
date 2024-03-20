import serial
import logging
import time

class UART:
    def __init__(self,
                 port='COM9',
                 baudrate=115200, #115200, 
                 timeout=0.5,
                 logger = None):
        
        # automatically connect to the first available port
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        self.esp32 = serial.Serial(baudrate=self.baudrate, timeout= self.timeout)

        # required delays for sending message
        self.timer_send = 0.003
        self.timer_recv = self.timer_send*2
        self.maximum_freq = 700 # hz

        if not logger:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def open(self):
        self.esp32.port=self.port
        self.esp32.close()
        self.esp32.open()
        self.logger.info(f"Opening {self.port} @ {self.baudrate} baudrate")

    def send(self, data:bytearray):
        self.esp32.write(data)

        # required delay
        t = time.perf_counter()
        while time.perf_counter() - t < self.timer_send:
            pass

    def receive(self):

        # required delay
        t = time.perf_counter()
        while time.perf_counter() - t < self.timer_recv:
            pass

        # check data
        if self.esp32.in_waiting == 65:
            msg_bytes = self.esp32.read(65)
            return msg_bytes
        elif self.esp32.in_waiting > 0: # clear buffer if not correct amount of data
            msg_bytes = self.esp32.read_all()
            self.logger.warning(f"Incorrect amount of data:{len(msg_bytes)} - clearing buffer")
            return None
        else: # non blocking
            return None            

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