# ------------------------------------------------------------------------------
# ---------------------------- Import Libraries --------------------------------
# ------------------------------------------------------------------------------
import time
import json
# Add the desired path to the system path
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("Project Root", PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)
# import ArtusAPI
from Sarcomere_Dynamics_Resources.ArtusAPI.artus_api import ArtusAPI

# Determine OS and run appropriate flash script
import platform
import subprocess

def example():
    input("""
        ╔══════════════════════════════════════════════════════════════════╗
        ║           Make sure ARTUS masterboard is in boot mode            ║
        ║                      Press Enter when ready                      ║
        ╚══════════════════════════════════════════════════════════════════╝
        """)
    # Prompt user for communication method and identifier
    communication_method = input(
        """
        ╔══════════════════════════════════════════════════════════════════╗
        ║                    Select Communication Method                   ║
        ╠══════════════════════════════════════════════════════════════════╣
        ║ Options:                                                         ║
        ║   1 -> UART                                                      ║
        ║   2 -> RS485                                                     ║
        ╚══════════════════════════════════════════════════════════════════╝
        >> Input Option (1-2): """
    )

    if communication_method == "1":
        communication_method = "UART"
    else:
        communication_method = "RS485"

    communication_channel_identifier = input("Enter COM port (e.g. COM3): ")

    artusapi = ArtusAPI(communication_method=communication_method,
        communication_channel_identifier=communication_channel_identifier,
        awake = True)

    # -------------------------------------------------------------------------------
    # --------------------------------- Example -------------------------------------
    # -------------------------------------------------------------------------------

    os_type = platform.system()

    if os_type == "Windows":
        flash_script = os.path.join(PROJECT_ROOT, "Sarcomere_Dynamics_Resources", "ArtusAPI", "firmware_update", "flash_script.bat") 
    elif os_type in ["Linux", "Darwin"]:
        flash_script = os.path.join(PROJECT_ROOT, "Sarcomere_Dynamics_Resources", "ArtusAPI", "firmware_update", "flash_script.sh")
    else:
        raise OSError(f"Unsupported operating system: {os_type}")

    print(f"\nRunning firmware update script for {os_type}...")

    try:
        # Run the flash script
        subprocess.run([flash_script], check=True, shell=True)
        print("Firmware update completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running firmware update script: {e}")
    except FileNotFoundError:
        print(f"Flash script not found at: {flash_script}")


    input("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║           Please restart the ARTUS hand in normal mode           ║
    ║                      Press Enter when ready                      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    artusapi.connect()

    periph = "periph.bin"
    act = "actuator.bin"
    fp = PROJECT_ROOT+"/Sarcomere_Dynamics_Resources/ArtusAPI/firmware_update/bins/"

    # update firmware for spi first
    artusapi.update_firmware(upload_flag='y', file_location=fp+periph, drivers_to_flash=9)
    artusapi.update_firmware(upload_flag='y', file_location=fp+act, drivers_to_flash=0)

    print("""
╔══════════════════════════════════════════════════════════════════╗
║             Firmware update completed successfully               ║
║        Please close this script and restart the ARTUS hand       ║
╚══════════════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    example()