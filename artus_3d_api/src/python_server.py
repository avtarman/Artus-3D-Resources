import socket
import time

class PythonServer:

    def __init__(self,
                 HEADER = 64,# Header size
                 FORMAT = "utf-8", # Format of the message
                 DISCONNECT_MESSAGE = "!DISCONNECT", # Disconnection message from the client
                 port= 5050,
                 reqReturnFlag= False,
                 DONECOMMAND = 211):
        
        self.HEADER = HEADER
        self.FORMAT = FORMAT
        self.DISCONNECT_MESSAGE = DISCONNECT_MESSAGE
        
        # get ip automatically
        self.server = socket.gethostbyname(socket.gethostname()) # 192.168.4.2
        # Port Number
        self.port = port
        # TCP tuple
        self.esp = (self.server,self.port)
        # create server
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        # self.server.setblocking(0)

        # bind server
        self.server.bind(self.esp)
        self.conn = None
        self.addr = None

    """ Start server and listen for connections """
    def start(self):
        # listen for connections
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.server}")
        # Accept the connection
        self.conn, self.addr = self.server.accept()
        print(f"[NEW CONNECTION] {self.addr} connected.")
        time.sleep(1)

        
    def recieve(self):
         # receive message of 1024 bytes (or an int)
        msg = self.conn.recv(1024).decode(self.FORMAT)
        return msg
    
    def send(self, command):
        # list to str
        # command = ','.join([str(x) for x in command])
        # add a \n at the end of the str
        command =  str(command)
        command += '\n'
        # send encoded data
        print(command)
        self.conn.send(command.encode(self.FORMAT))