
class ArtusLite:

    def __init__(self,
                joint_max_angles=[35, 90, 90, 90, # thumb
                                20, 90, 90, # index
                                20, 90, 90, # middle
                                20, 90, 90, # ring
                                20, 90, 90], # pinky
                joint_min_angles=[-35, 0, 0, 0, # thumb
                                -20, 0, 0, # index
                                -20, 0, 0, # middle
                                -20, 0, 0, # ring
                                -20, 0, 0], # pinky

                joint_default_angles=[0, 0, 0, 0, # thumb
                                    0, 0, 0, # index
                                    0, 0, 0, # middle
                                    0, 0, 0, # ring
                                    0, 0, 0], # pinky

                joint_rotation_directions=[1, 1, 1, 1, # thumb
                                        1, 1, 1, # index
                                        1, 1, 1, # middle
                                        1, 1, 1, # ring
                                        1, 1, 1], # pinky

                joint_velocities=[0, 0, 0, 0, # thumb
                                0, 0, 0, # index
                                0, 0, 0, # middle
                                0, 0, 0, # ring
                                0, 0, 0], # pinky

                number_of_joints=16
    ):

        self.joint_max_angles = joint_max_angles
        self.joint_min_angles = joint_min_angles
        self.joint_default_angles = joint_default_angles
        self.joint_rotation_directions = joint_rotation_directions
        self.joint_velocities = joint_velocities
        self.number_of_joints = number_of_joints

        class Joint:
            def __init__(self, index, min_angle, max_angle, default_angle, target_angle, current_angle, rotation_direction, velocity, temperature):
                self.index = index
                self.min_angle = min_angle
                self.max_angle = max_angle
                self.default_angle = default_angle
                self.target_angle = target_angle
                self.current_angle = current_angle
                self.rotation_direction = rotation_direction
                self.velocity = velocity
                self.temperature = temperature
        self.Joint = Joint

        self._create_hand()



    def _create_hand(self):
        """
        Creates the hand with all its fingers and joints
        """
        self.hand_joints = []
        for joint_index in range(self.number_of_joints):
            joint = self.Joint(index=joint_index,
                            min_angle=self.joint_min_angles[joint_index],
                            max_angle=self.joint_max_angles[joint_index],
                            default_angle=self.joint_default_angles[joint_index],
                            target_angle=self.joint_default_angles[joint_index],
                            current_angle=self.joint_default_angles[joint_index],
                            rotation_direction=self.joint_rotation_directions[joint_index],
                            velocity=self.joint_velocities[joint_index],
                            temperature=0)
            self.hand_joints.append(joint)


        def __str__(self):
            return str(self.hand_joints)
        

    def set_joint_angles(self, joint_angles):
        """
        Set the joint angles of the hand
        """

        
        joint_angles = self._check_joint_limits(joint_angles) # check if the joint angles are within the limits
        # set the joint angles
        for joint in self.hand_joints:
            joint.target_angle = joint_angles[joint.index]
        # convert the joint angles to the hand angles (list)
        joint_angles = [joint.target_angle for joint in self.hand_joints]
        return joint_angles
    
    def _check_joint_limits(self, joint_angles):
        """
        Check if the joint angles are within the limits
        """
        for joint in self.hand_joints:
            if joint_angles[joint.index] > joint.max_angle:
                joint_angles[joint.index] = joint.max_angle
            if joint_angles[joint.index] < joint.min_angle:
                joint_angles[joint.index] = joint.min_angle
        return joint_angles
    

    def set_home_position(self):
        """
        Set the hand to the home position
        """
        joint_angles = [joint.default_angle for joint in self.hand_joints]
        return self.set_joint_angles(joint_angles)
    
    def get_joint_angles(self, joint_angles):
        """
        Get the joint angles of the hand
        """
        return joint_angles


def main():
    artus_lite = ArtusLite()
    print(artus_lite)
    print(artus_lite.hand_joints)
    print(len(artus_lite.hand_joints))


def print_finger_joint_limits():
    artus_lite = ArtusLite()
    for joint in artus_lite.hand_joints:
        print(joint.index, joint.min_angle, joint.max_angle)
if __name__ == "__main__":
    # main()
    print_finger_joint_limits()
