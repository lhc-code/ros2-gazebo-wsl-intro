import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ParamTalker(Node):
    def __init__(self):
        super().__init__('param_talker')
        self.declare_parameter('message', '기본 메시지')  # parameter 이름, 기본값
        self.declare_parameter('period', 1.0)
        self.pub = self.create_publisher(String, 'chatter', 10)
        period = self.get_parameter('period').value
        self.timer = self.create_timer(period, self.on_timer)

    def on_timer(self):
        msg = String()
        msg.data = self.get_parameter('message').value  # 매번 읽으므로 실행 중 변경이 바로 반영됨
        self.pub.publish(msg)
        self.get_logger().info(f'보냄: {msg.data}')


def main():
    rclpy.init()
    node = ParamTalker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
