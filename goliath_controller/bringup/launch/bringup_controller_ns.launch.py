from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "namespace",
            default_value="robot_1",    #change this for every new robot 
            description="Namespace for the robot",
        ),
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

    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    gui = LaunchConfiguration("gui")
    controller_manager_path = PathJoinSubstitution(
    [namespace, "controller_manager"]
)
    # Controller config
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("goliath_controller"),
            "config",
            "goliath_controller_ns_1.yaml",     #change for every new robot 
        ]
    )

    # Controller manager
    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        namespace=namespace,
        parameters=[robot_controllers, {"use_sim_time": use_sim_time}],
        remappings=[
            ("~/robot_description", "robot_description"),
        ],
        output="both",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        #namespace=namespace,
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            controller_manager_path,
        ],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        #namespace=namespace,
        arguments=[
            "position_controller",  
            "--controller-manager",
            controller_manager_path,
        ],
    )

    return LaunchDescription(
        declared_arguments +
        [
            control_node,
            joint_state_broadcaster_spawner,
            robot_controller_spawner,

        ]
    )
