from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_path = os.path.join(
        get_package_share_directory('artuslite_ros_api'),
        'config',
        'artuslite_params.yaml'
    )

    return LaunchDescription([
        Node(
            package='artuslite_ros_api',
            executable='artuslite_ros_node',
            name='artuslite_ros_node',
            parameters=[config_path]
        )
    ])
