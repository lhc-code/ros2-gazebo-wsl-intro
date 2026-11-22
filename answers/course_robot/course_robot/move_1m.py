import math

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node


class Move1m(Node):
    def __init__(self):
        super().__init__('move_1m')
        self.declare_parameter('distance', 1.0)  # 이동할 거리 [m]
        self.declare_parameter('speed', 0.2)     # 전진 속도 [m/s]
        self.start = None  # 처음 받은 위치 (x, y)
        self.done = False
        self.create_subscription(Odometry, '/odom', self.on_odom, 10)
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def on_odom(self, msg):
        if self.done:
            return
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        if self.start is None:
            self.start = (x, y)
            self.get_logger().info(f'출발: x={x:.2f}, y={y:.2f}')
        moved = math.hypot(x - self.start[0], y - self.start[1])  # 출발점에서 떨어진 거리
        cmd = Twist()
        if moved < self.get_parameter('distance').value:
            cmd.linear.x = self.get_parameter('speed').value
        else:
            self.done = True
            self.get_logger().info(f'정지: {moved:.3f} m 이동')
        self.pub.publish(cmd)  # 목표 도달 시 속도 0을 보내 정지


def main():
    rclpy.init()
    node = Move1m()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(Twist())  # 종료할 때도 정지 명령
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
