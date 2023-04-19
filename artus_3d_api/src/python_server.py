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
        # flags
        self.reqReturnFlag = reqReturnFlag
        # msg
        self.twosend = [0] * 16
        self.msg = 'hello'
        self.DONECOMMAND = DONECOMMAND



    """ Start server and listen for connections """
    def start(self):
        # listen for connections
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.server}")
        # Accept the connection
        self.conn, self.addr = self.server.accept()



    """ 
        Receive integer from client
        @returns -> whether or not the command is complete or not
    """
    def recvInt(self):
        # receive message of 4 bytes (or an int)
        msg = self.conn.recv(4).decode(self.FORMAT)
        if '\r\n' in msg:
            msg = msg.strip('\r\n')
        if msg != '':
            msg = int(msg)
        time.sleep(0.1)
        if msg == self.DONECOMMAND:
            print('=====\n\n[STAT] Message Received!!\n\n=====')
            return True
        else:
            return False

    """
        send array to client
    """
    def send(self, command):
        # list to str
        # command = ','.join([str(x) for x in command])
        # add a \n at the end of the str
        command =  str(command)
        command += '\n'
        # send encoded data
        print(command)
        self.conn.send(command.encode(self.FORMAT))


def main():
    server = PythonServer()
    server.start()
    while True:
        server.send([0] * 16)


if __name__ == '__main__':
    main()