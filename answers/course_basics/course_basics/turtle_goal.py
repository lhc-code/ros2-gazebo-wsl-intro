import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from turtlesim.msg import Pose


class TurtleGoal(Node):
    def __init__(self):
        super().__init__('turtle_goal')
        self.declare_parameter('goal_x', 8.0)  # turtlesim 화면은 0 ~ 11
        self.declare_parameter('goal_y', 8.0)
        self.pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_pose(self, msg):
        self.pose = msg

    def on_timer(self):
        if self.pose is None:
            return
        gx = self.get_parameter('goal_x').value
        gy = self.get_parameter('goal_y').value
        dx, dy = gx - self.pose.x, gy - self.pose.y
        dist = math.hypot(dx, dy)
        cmd = Twist()
        if dist > 0.1:  # 목표까지 0.1 이상 남았으면 이동
            angle_err = math.atan2(dy, dx) - self.pose.theta
            angle_err = math.atan2(math.sin(angle_err), math.cos(angle_err))  # -pi ~ pi로 정리
            cmd.angular.z = 4.0 * angle_err
            if abs(angle_err) < 0.3:  # 방향이 대충 맞으면 전진
                cmd.linear.x = min(1.5 * dist, 2.0)
        else:
            self.get_logger().info('도착', once=True)
        self.pub.publish(cmd)


def main():
    rclpy.init()
    node = TurtleGoal()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
