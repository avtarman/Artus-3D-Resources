

# import sys
# from pathlib import Path
# # Current file's directory
# current_file_path = Path(__file__).resolve()
# # Add the desired path to the system path
# desired_path = current_file_path.parent.parent.parent.parent
# sys.path.append(str(desired_path))
# print(desired_path)

# # Artus Lite Robots
# from ArtusAPI.robot.artus_lite.artus_lite_left import ArtusLite_LeftHand
# from ArtusAPI.robot.artus_lite.artus_lite_right import ArtusLite_RightHand

from .artus_lite.artus_lite_left import ArtusLite_LeftHand
from .artus_lite.artus_lite_right import ArtusLite_RightHand

# Artus 3D Robots


class Robot:
    def __init__(self,
                 robot_type='artus_lite',
                hand_type='left'):
        
        # initialize robot
        self.robot_type = robot_type
        self.hand_type = hand_type
        # setup robot
        self.robot = None
        self._setup_robot()

    def _setup_robot(self):
        """
        Initialize robot based on the robot type and hand type
        """
        # setup robot based on the hand
        if self.robot_type == 'artus_lite':
            if self.hand_type == 'left':
                self.robot = ArtusLite_LeftHand()
            elif self.hand_type == 'right':
                self.robot = ArtusLite_RightHand()
            else:
                raise ValueError("Unknown hand")
        else:
            raise ValueError("Unknown robot type")
        

    def set_joint_angles(self, joint_angles:dict,name:bool):
        """
        Set the joint angles of the hand
        """
        if name:
            return self.robot.set_joint_angles_by_name(joint_angles)
        else:
            return self.robot.set_joint_angles(joint_angles)
    
    
    def set_home_position(self):
        """
        Set the hand to the home position
        """
        return self.robot.set_home_position()
    
    def get_joint_angles(self, joint_angles):
        """
        Get the joint angles of the hand
        """
        return self.robot.get_joint_angles(joint_angles)
    

def main():
    artus_robot = Robot(hand_type='left')

if __name__ == "__main__":
    main()