![9xawu8](https://github.com/user-attachments/assets/f2ed8419-ab4c-40d2-b13c-0d9abf2d650d)


goliath linear manual 


Check if both USB connections are made for the arm & for the gripper
ls -l /dev/ttyACM* && ls -l /dev/ttyUSB*

home the robot:
echo "HOME" > /dev/ttyUSB0

testing the robot with ros2 control 
ros2 launch goliath_controller goliath_controller.launch.py 

test line direct position commands 
ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray "data: [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.1]" 
                                                                                    j1   j2   j3   j4   j5   j6   rail
back to zero before closing 
ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray "data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"


while true; do ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray "data: [-1.5775, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2]" --once; sleep 5; ros2 topic pub /position_controller/commands std_msgs/msg/Float64MultiArray "data: [1.5775, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]" --once; sleep 5; done;


RUN MOVEIT 
ros2 launch moveit_include demo.launch.py 

RUN MOVEIT COMMANDER
First run the Commander API
ros2 run my_robot_commander_cpp commander 

command joint positions on topic

command predefined pose on topic 

command end effectpose and position on topic 

command gripper open or close 

