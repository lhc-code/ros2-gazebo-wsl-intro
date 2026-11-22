import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.pub = self.create_publisher(String, 'chatter', 10)  # topic 이름 chatter
        self.count = 0
        self.timer = self.create_timer(0.5, self.on_timer)  # 0.5초마다 on_timer 실행

    def on_timer(self):
        msg = String()
        msg.data = f'안녕 ROS2 {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(f'보냄: {msg.data}')
        self.count += 1


def main():
    rclpy.init()
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
