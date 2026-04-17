from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "gui",
            default_value="false",
            description="Start RViz2 automatically",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use simulation time",
        ),
    ]
           
    use_sim_time = LaunchConfiguration("use_sim_time")
    gui = LaunchConfiguration("gui")

    # Controller config
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("goliath_controller"),
            "config",
            "goliath_controller.yaml",
        ]
    )

    # Controller manager
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        
        parameters=[robot_controllers, {"use_sim_time": use_sim_time}],
        remappings=[
            ("~/robot_description", "robot_description"),
        ],
        output="both",
    )

    # Spawners (IMPORTANT: use full namespaced path)
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster", "--controller-manager", "/controller_manager"],
     
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "position_controller", "--controller-manager", "/controller_manager"],
    )

    
    return LaunchDescription(
        declared_arguments +
        [
            control_node,
            joint_state_broadcaster_spawner,
            robot_controller_spawner,
            
        ]
    )
