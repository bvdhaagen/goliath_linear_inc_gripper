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
            default_value="robot_2",
            description="Namespace for the robot (anything will do)",
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
    ["/", namespace, "controller_manager"]
)
    # Controller config
    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("goliath_controller"),
            "config",
            "goliath_controller_ns_2.yaml",
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
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            controller_manager_path,
        ],
    )

    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "position_controller",  # must match YAML
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
