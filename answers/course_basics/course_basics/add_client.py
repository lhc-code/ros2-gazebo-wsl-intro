import sys

import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


class AddClient(Node):
    def __init__(self):
        super().__init__('add_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):  # server가 켜질 때까지 대기
            self.get_logger().info('server 기다리는 중...')

    def send(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)  # 응답이 올 때까지 대기
        return future.result()


def main():
    if len(sys.argv) != 3:
        print('숫자 2개를 넣으세요. 예: add_client 3 5')
        return
    rclpy.init()
    node = AddClient()
    result = node.send(int(sys.argv[1]), int(sys.argv[2]))
    node.get_logger().info(f'결과: {result.sum}')
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
