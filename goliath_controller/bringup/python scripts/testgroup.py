#!/usr/bin/env python3
import random
import time
import subprocess
import math

# 3 robots met verschillende posities (x, y)
robots = {
    "robot_1": {"x": 0.0, "y": 0.0},      # Center
    "robot_2": {"x": 1.2, "y": 0.0},      # Rechts
    "robot_3": {"x": -1.2, "y": 0.0}      # Links
}

# Start static transforms voor alle robots
print("📡 Starting static transforms...")
for robot, pos in robots.items():
    cmd = [
        'ros2', 'run', 'tf2_ros', 'static_transform_publisher',
        str(pos['x']), str(pos['y']), '0',  # x, y, z
        '0', '0', '0',                      # roll, pitch, yaw
        'world',                            # parent frame
        f'{robot}/base_link_linear'         # child frame
    ]
    subprocess.Popen(cmd)
    print(f"  {robot} at position ({pos['x']}, {pos['y']})")

time.sleep(1)
print("✅ TF transforms active\n")

def send_command(robot, positions):
    """Send position command to a robot"""
    pos_str = ", ".join(f"{p:.3f}" for p in positions)
    cmd = f'ros2 topic pub {robot}/position_controller/commands std_msgs/msg/Float64MultiArray "data: [{pos_str}]" --once'
    subprocess.Popen(cmd, shell=True)

def random_pose():
    """Generate random joint positions"""
    return [
        random.uniform(-3.14, 3.14),  # joint_1
        random.uniform(-1.57, 1.57),  # joint_2
        random.uniform(-2.6, 2.6),    # joint_3
        random.uniform(-3.14, 3.14),  # joint_4
        random.uniform(-2.09, 2.09),  # joint_5
        random.uniform(-3.14, 3.14),  # joint_6
        random.uniform(-0.455, 0.455), # slider_11
        random.uniform(-0.003, 0.022), # Slider_22
        random.uniform(-0.022, 0.003)  # Slider_23
    ]

print("🎲 Starting random robot movements for 3 robots...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        # Generate 3 random poses (one for each robot)
        poses = [random_pose() for _ in range(3)]
        
        # Send 5 sequences
        for seq in range(5):
            # Elke robot krijgt een andere pose
            for i, robot in enumerate(robots.keys()):
                send_command(robot, poses[i])
            
            print(f"  Sequence {seq+1}/5 sent to all robots")
            time.sleep(0.3)  # 0.3 second tussen poses
            
            # Genereer nieuwe poses voor de volgende sequence
            poses = [random_pose() for _ in range(3)]
        
        print(f"  ✅ Cycle complete. Starting new in 2 seconds...\n")
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n\n⏹️  Stopping. Sending home position...")
    home = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for robot in robots.keys():
        send_command(robot, home)
    print("✅ Done - all robots at home position")
