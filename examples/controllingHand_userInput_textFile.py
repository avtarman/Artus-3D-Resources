import time





import sys
from pathlib import Path
# Current file's directory
current_file_path = Path(__file__).resolve()
# Add the desired path to the system path
desired_path = current_file_path.parent.parent
sys.path.append(str(desired_path))
print(desired_path)

from ArtusAPI.artus_api import ArtusAPI

def main_menu():
    return input('''
Artus 3D API 1.0
Command options:
1. start connection to hand
2. close connection
3. wakeup hand
4. sleep hand
5. calibrate
6. send command from grasp_patterns/example_command.txt
7. save grasp pattern to file
8. use grasp pattern from file
9. get robot states
10. ~ reset finger ~
11. open hand from grasp_patterns/grasp_open.txt
12. close hand using grasp in grasp_patterns/grasp.txt
13. firmware flash actuators
14. save current hand state for power cycle
Enter command: ''')

def example():
    artus3d = ArtusAPI()
    while True:
        user_input = main_menu()
        match user_input:
            case "1":
                artus3d.start_connection()
            case "2":
                artus3d.wakeup()
            case "3":
                artus3d.calibrate()
            case "4":
                with open(os.path.join("grasp_patterns","example_command.txt"), "r") as f:
                    command = f.read()
                artus3d.send_target_command(command)
            case "5":
                artus3d.save_grasp_pattern()
            case "6":
                artus3d.get_grasp_pattern()
            case "7":
                artus3d.get_robot_states()
            case "8": 
                joint = input('choose joint angle 0-16: ')
                user_act = input("choose actuator:\n0:both\n1:act1\n2:act2")
                artus3d.locked_reset_low(joint,user_act)
            case "9":
                with open(os.path.join("grasp_patterns","grasp_open.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send(command)
            case "10":
                with open(os.path.join("grasp_patterns","grasp.txt"), "r") as f:
                    command = f.read()
                if command != "":
                    artus3d.send(command)
            case "11":
                artus3d.flash_file() 
            case "12":
                artus3d.sleep()
            case "13":
                artus3d.close_connection()       

if __name__ == '__main__':
    example()


