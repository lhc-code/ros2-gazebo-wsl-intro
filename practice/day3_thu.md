# 3일차 (목) - ROS2 통신과 Gazebo 이동 로봇

| 차시 | 시간 | 내용 |
|---|---|---|
| 1 | 09:00 ~ 09:50 | service server · client 작성 |
| 2 | 10:00 ~ 10:50 | parameter · launch 파일 작성 |
| 3 | 11:00 ~ 11:50 | Turtlesim 거북이 목표점 이동 |
| - | 12:00 ~ 13:00 | 점심 |
| 4 | 13:00 ~ 13:50 | URDF 로봇 모델 작성 및 RViz 확인 |
| 5 | 14:00 ~ 14:50 | Gazebo에 로봇 불러오기 및 키보드 주행 |
| 6 | 15:00 ~ 15:50 | Gazebo 로봇 1m 이동 node 작성 및 정리 |

2일차에 만든 `my_first_pkg`에 이어서 작성합니다.

---

## 1차시 - service

topic은 계속 흘려보내는 방송, **service**는 요청 1번에 응답 1번인 질문·대답입니다. 두 수를 보내면 합을 돌려주는 service를 만듭니다.

### 1-1. 의존성 추가

Ubuntu 터미널
```bash
gedit ~/ros2_ws/src/my_first_pkg/package.xml
```
`<depend>std_msgs</depend>` 아래에 한 줄 추가합니다.
```xml
  <depend>example_interfaces</depend>
```

### 1-2. server 작성 - `my_first_pkg/add_server.py`

<!-- sync: answers/course_basics/course_basics/add_server.py -->
```python
import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


class AddServer(Node):
    def __init__(self):
        super().__init__('add_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.on_request)

    def on_request(self, request, response):  # 요청 1번에 응답 1번
        response.sum = request.a + request.b
        self.get_logger().info(f'{request.a} + {request.b} = {response.sum}')
        return response


def main():
    rclpy.init()
    node = AddServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

### 1-3. client 작성 - `my_first_pkg/add_client.py`

<!-- sync: answers/course_basics/course_basics/add_client.py -->
```python
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
```

### 1-4. 등록 · build · 실행

`setup.py`의 `console_scripts`에 두 줄 추가합니다.
```python
            'add_server = my_first_pkg.add_server:main',
            'add_client = my_first_pkg.add_client:main',
```

Ubuntu 터미널 ①
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_first_pkg
source install/local_setup.bash
ros2 run my_first_pkg add_server
```

Ubuntu 터미널 ②
```bash
ros2 run my_first_pkg add_client 3 5
```
- 성공: ②에 `결과: 8`, ①에 `3 + 5 = 8`.

명령어로도 요청할 수 있습니다.

Ubuntu 터미널 ②
```bash
ros2 service list
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 20}"
```

---

## 2차시 - parameter와 launch

**parameter** = 코드를 고치지 않고 바꿀 수 있는 설정값. **launch** 파일 = 여러 node를 명령 한 번에 실행.

### 2-1. parameter node - `my_first_pkg/param_talker.py`

<!-- sync: answers/course_basics/course_basics/param_talker.py -->
```python
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
```

`setup.py`에 `'param_talker = my_first_pkg.param_talker:main',`을 추가하고 build합니다.

Ubuntu 터미널 ①
```bash
ros2 run my_first_pkg param_talker
```

Ubuntu 터미널 ②
```bash
ros2 param list /param_talker
ros2 param set /param_talker message "실행 중에 바꾼 메시지"
```
- 성공: ①의 출력 문장이 바로 바뀜.

실행할 때 처음부터 값을 넣을 수도 있습니다.
```bash
ros2 run my_first_pkg param_talker --ros-args -p message:="처음부터 다른 메시지" -p period:=0.5
```

### 2-2. 설정 파일 - `my_first_pkg/config/talker.yaml`

Ubuntu 터미널
```bash
mkdir -p ~/ros2_ws/src/my_first_pkg/config ~/ros2_ws/src/my_first_pkg/launch
gedit ~/ros2_ws/src/my_first_pkg/config/talker.yaml
```

<!-- sync: answers/course_basics/config/talker.yaml -->
```yaml
param_talker:
  ros__parameters:
    message: "launch 파일에서 넣은 메시지"
    period: 0.5
```

### 2-3. launch 파일 - `my_first_pkg/launch/talker_listener.launch.py`

정답 코드의 `'course_basics'` 세 곳을 `'my_first_pkg'`로 바꿔서 씁니다.

<!-- sync: answers/course_basics/launch/talker_listener.launch.py -->
```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(get_package_share_directory('course_basics'), 'config', 'talker.yaml')
    return LaunchDescription([
        Node(package='course_basics', executable='param_talker', parameters=[config], output='screen'),
        Node(package='course_basics', executable='listener', output='screen'),
    ])
```

### 2-4. `setup.py`에 launch · config 폴더 등록

`setup.py` 맨 위에 추가:
```python
from glob import glob
```
`data_files` 리스트에 두 줄 추가:
```python
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
```

Ubuntu 터미널
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_first_pkg
source install/local_setup.bash
ros2 launch my_first_pkg talker_listener.launch.py
```
- 성공: 한 터미널에 `보냄: launch 파일에서 넣은 메시지`와 `받음: ...`이 번갈아 출력됨.

---

## 3차시 - 거북이 목표점 이동

거북이 위치(`/turtle1/pose`)를 받아서, 목표점 방향으로 돌고 전진하는 속도(`/turtle1/cmd_vel`)를 보냅니다. 1·2일차에 배운 subscriber + publisher + parameter를 모두 씁니다.

`package.xml`에 의존성 두 줄 추가:
```xml
  <depend>geometry_msgs</depend>
  <depend>turtlesim</depend>
```

### 3-1. `my_first_pkg/turtle_goal.py`

<!-- sync: answers/course_basics/course_basics/turtle_goal.py -->
```python
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
```

`setup.py`에 `'turtle_goal = my_first_pkg.turtle_goal:main',` 추가 후 build.

Ubuntu 터미널 ①
```bash
ros2 run turtlesim turtlesim_node
```

Ubuntu 터미널 ②
```bash
ros2 run my_first_pkg turtle_goal --ros-args -p goal_x:=2.0 -p goal_y:=9.0
```
- 성공: 거북이가 왼쪽 위로 이동 후 멈추고 `도착` 출력.
- 숫자는 `2.0`처럼 소수점까지 씁니다. `2`라고 쓰면 정수로 인식되어 오류가 납니다.

실행 중 목표 바꾸기:

Ubuntu 터미널 ③
```bash
ros2 param set /turtle_goal goal_x 9.0
ros2 param set /turtle_goal goal_y 2.0
```

**확인 질문**: `cmd.angular.z = 4.0 * angle_err`에서 4.0을 1.0으로 바꾸면 어떻게 될까요?
<details><summary>답</summary>

방향을 천천히 돌려서 도착까지 더 오래 걸림. 너무 크게 하면 좌우로 흔들림.
</details>

---

## 4차시 - URDF 로봇 모델과 RViz

**URDF** = 로봇의 모양(link)과 연결(joint)을 적은 XML 파일. 이 저장소의 `course_robot` package에 2륜 로봇이 들어 있습니다.

```
base_footprint (바닥 기준점)
└── base_link (파란 몸체)
    ├── left_wheel   (continuous joint: 계속 회전)
    ├── right_wheel  (continuous joint)
    └── caster       (fixed joint: 앞쪽 보조 바퀴)
```

### 4-1. RViz로 보기

Ubuntu 터미널
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select course_robot
source install/local_setup.bash
ros2 launch course_robot display.launch.py
```
- 성공: RViz 창에 파란 상자 + 검은 바퀴 2개. 작은 슬라이더 창에서 바퀴 joint를 움직이면 바퀴가 돕니다.
- RViz에서 마우스 왼쪽 드래그 = 회전, 휠 = 확대.

### 4-2. 로봇 모양 바꾸기

Ubuntu 터미널
```bash
gedit ~/ros2_ws/src/ros2-gazebo-wsl-intro/answers/course_robot/urdf/simple_bot.urdf.xacro
```

파일 위쪽 "학생이 바꿔볼 값"을 바꿔봅니다.

| 값 | 기본 | 바꿔볼 예 |
|---|---|---|
| `body_x` | 0.40 | 0.60 (몸체 길게) |
| `wheel_r` | 0.06 | 0.10 (바퀴 크게) |
| `blue` 색 `rgba` | `0.1 0.3 0.8 1` | `0.8 0.2 0.2 1` (빨강) |

저장 후 RViz를 끄고(`Ctrl + C`) 4-1의 launch 명령을 다시 실행합니다.

**확인 질문**: 바퀴 joint가 `fixed`라면 어떻게 될까요?
<details><summary>답</summary>

바퀴가 몸체에 고정되어 회전하지 않음. 슬라이더 창에도 나타나지 않음.
</details>

---

## 5차시 - Gazebo에서 로봇 주행

RViz는 **보여주기만** 하고, Gazebo는 중력·마찰이 있는 **물리 시뮬레이터**입니다.

### 5-1. Gazebo 실행

Ubuntu 터미널 ①
```bash
ros2 launch course_robot gazebo.launch.py
```
- 성공: Gazebo 창에 회색 바닥, 초록 선(출발), 빨간 선(1m), 파란 로봇.
- CPU 렌더링이라 창이 뜨기까지 30초 이상 걸릴 수 있습니다. [미검증: 실습실 PC 실측 필요]
- 화면이 검거나 바로 꺼지면:
  ```bash
  ros2 launch course_robot gazebo.launch.py render_engine:=ogre
  ```

### 5-2. 키보드로 주행

Ubuntu 터미널 ②
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

| 키 | 동작 |
|---|---|
| `i` | 전진 |
| `,` | 후진 |
| `j` / `l` | 제자리 왼쪽 / 오른쪽 회전 |
| `k` | 정지 |
| `q` / `z` | 속도 올리기 / 내리기 |

- 터미널 ②를 클릭한 상태에서 눌러야 합니다.

### 5-3. 무엇이 오가는지 확인

Ubuntu 터미널 ③
```bash
ros2 topic list
ros2 topic echo /cmd_vel
ros2 topic echo /odom --field pose.pose.position
```
- `/cmd_vel`: 키보드 node → 로봇 (속도 명령)
- `/odom`: 로봇 → ROS2 (현재 위치)
- 거북이 때와 같은 구조입니다. topic 이름만 다릅니다.

---

## 6차시 - 1m 이동 node와 정리

`/odom`으로 위치를 받아, 출발점에서 1m 멀어지면 멈추는 node를 만듭니다.

`package.xml`에 의존성 추가:
```xml
  <depend>nav_msgs</depend>
```

### 6-1. `my_first_pkg/move_1m.py`

<!-- sync: answers/course_robot/course_robot/move_1m.py -->
```python
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
```

`setup.py`에 `'move_1m = my_first_pkg.move_1m:main',` 추가 후 build.

### 6-2. 실행

Gazebo를 다시 켜서 로봇을 출발선에 둡니다(5-1). 키보드 node는 끕니다.

Ubuntu 터미널 ②
```bash
ros2 run my_first_pkg move_1m
```
- 성공: 로봇이 직진해 빨간 선 근처에서 멈추고 `정지: 1.0xx m 이동` 출력.

거리와 속도 바꿔보기:
```bash
ros2 run my_first_pkg move_1m --ros-args -p distance:=0.5 -p speed:=0.4
```

**확인 질문**: 속도를 높이면 멈춘 위치가 목표보다 더 멀어지는 이유는?
<details><summary>답</summary>

odom이 오는 간격 동안에도 로봇이 움직이고, 정지 명령 후에도 관성으로 조금 미끄러지기 때문. 실제 로봇은 목표 근처에서 감속해서 이 문제를 줄임.
</details>

### 6-3. 3일 정리

| 개념 | 한 줄 요약 | 이번 과정에서 쓴 예 |
|---|---|---|
| node | 하나의 실행 프로그램 | talker, turtle_goal, move_1m |
| topic | 계속 흘려보내는 메시지 통로 | `/chatter`, `/turtle1/cmd_vel`, `/odom` |
| service | 요청 1번 → 응답 1번 | `/add_two_ints` |
| parameter | 코드 수정 없이 바꾸는 설정값 | `goal_x`, `distance` |
| launch | 여러 node 한 번에 실행 | `gazebo.launch.py` |
| URDF | 로봇 모양·연결 정의 | `simple_bot.urdf.xacro` |

| 명령 | 용도 |
|---|---|
| `ros2 run <package> <실행이름>` | node 실행 |
| `ros2 launch <package> <launch파일>` | launch 실행 |
| `ros2 node list` / `ros2 topic list` | 실행 중인 node / topic |
| `ros2 topic echo <topic>` | topic 내용 보기 |
| `ros2 param set <node> <이름> <값>` | parameter 바꾸기 |
| `colcon build --symlink-install` | build |

## 선택 과제 (빨리 끝난 사람)

카메라 달기 - CPU 렌더링이라 느릴 수 있습니다.

Ubuntu 터미널 ①
```bash
ros2 launch course_robot gazebo.launch.py use_camera:=true
```

Ubuntu 터미널 ②
```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

## 문제 해결

| 증상 | 조치 |
|---|---|
| `ModuleNotFoundError: example_interfaces` 등 | `package.xml`에 의존성 추가 후 다시 build |
| launch 파일을 못 찾음 | `setup.py`의 `data_files`에 launch 줄 추가 후 다시 build |
| `InvalidParameterTypeException` | 숫자 parameter는 `2.0`처럼 소수점까지 |
| Gazebo에서 로봇이 안 움직임 | `ros2 topic list`에 `/cmd_vel`이 있는지, teleop 터미널을 클릭했는지 확인 |
| move_1m이 바로 `정지` | Gazebo가 켜져 있는지, `/odom`이 오는지(`ros2 topic hz /odom`) 확인 |
| Gazebo가 매우 느림 | 다른 프로그램 종료, `setup/README.md`의 `.wslconfig`로 메모리 늘리기 |
