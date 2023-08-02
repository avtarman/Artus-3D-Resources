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
        self.server_socket = None
        self.conn = None
        self.addr = None

        self.msg = ""

    """ Start server and listen for connections """
    def start(self):
        # create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.esp)

        # listen for connections
        self.server_socket.listen()
        print(f"[LISTENING] Server is listening on  {self.server}:{self.port}")
        # Accept the connection
        self.conn, self.addr = self.server_socket.accept()
        print(f"[NEW CONNECTION] {self.addr} connected.")
        time.sleep(1)

        
    def receive(self):
         # receive message of 1024 bytes (or an int)
        
        msg = self.conn.recv(1024).decode(self.FORMAT)
        ## TODO: make sure the packet is complete
        if msg != self.msg:
            self.msg = msg
            return msg
        return ""
    
    def send(self, command):
        # list to str
        # command = ','.join([str(x) for x in command])
        # add a \n at the end of the str
        command =  str(command)
        command += '\n'
        # send encoded data
        print(command)
        self.conn.send(command.encode(self.FORMAT))

    def sendBytes(self,command):
        self.conn.send(command)
    
    def close(self):
        if self.conn:
            self.conn.close()
        if self.server_socket:
            self.server_socket.close()
        self.conn = None
        self.addr = None
        print("[SERVER CLOSED]")