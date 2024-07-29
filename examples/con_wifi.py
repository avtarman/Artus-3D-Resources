import time
import json
import os
import sys
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent
sys.path.append(str(desired_path))

from ArtusAPI.artus_api import ArtusAPI

artus = ArtusAPI(communication_method='WiFi', communication_channel_identifier='ArtusLite_R')

try:
    artus.connect()
    
    while True:
        artus._communication_handler.receive_data()
        time.sleep(1)

except Exception as e:
    print(e)

