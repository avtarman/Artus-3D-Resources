
class FirmwareUpdater:

    def __init__(self,
                 communication_handler= None,
                 file_location = ""
                    ):
        
        self.communication_handler = communication_handler
        self.file_location = file_location


    def update_firmware(self, communication_handler):
        acknowledged = False

        file_location = self.file_location
        file_size = os.path.getsize(file_location) 

        self.communication_handler.send("file ready\n".encode())
        self.communication_handler.send((str(file_size)+"\n").encode())


        file = open(file_location, "rb")
        file_data = file.read()
        file.close

        self.communication_handler.sendall(file_data)

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
            else:
                print(message)


def test_firmware_updater():
    firmware_updater = FirmwareUpdater()
    firmware_updater.update_firmware(communication_handler=None)

if __name__ == "__main__":
    test_firmware_updater()