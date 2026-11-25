# 2일차 (수, 오전) - ROS2 첫걸음

| 차시 | 시간 | 내용 |
|---|---|---|
| 1 | 09:00 ~ 09:50 | WSL Ubuntu 터미널 사용법 & ROS2 소개 |
| 2 | 10:00 ~ 10:50 | ROS2 package 생성 및 node 실행 |
| 3 | 11:00 ~ 11:50 | publisher · subscriber 작성 |

시작 전 확인: [setup/README.md](../setup/README.md) 설치와 진단 스크립트가 끝나 있어야 합니다.

---

## 1차시 - 터미널과 ROS2 소개

### 1-1. Ubuntu 터미널 열기

Windows 시작 메뉴에서 **Ubuntu 24.04**를 실행합니다. 검은 창이 Linux 터미널입니다.

### 1-2. 기본 명령어

Ubuntu 터미널
```bash
pwd                # 지금 위치
ls                 # 현재 폴더 내용
mkdir practice     # 폴더 만들기
cd practice        # 폴더로 들어가기
echo "hello" > a.txt
cat a.txt          # 파일 내용 보기
cd ..              # 위 폴더로
```

| 명령 | 뜻 |
|---|---|
| `pwd` | 현재 위치 출력 |
| `ls` | 폴더 내용 보기 |
| `cd 폴더` / `cd ..` / `cd ~` | 이동 / 위로 / 홈으로 |
| `mkdir 폴더` | 폴더 만들기 |
| `Tab` 키 | 이름 자동 완성 |
| `↑` 키 | 이전 명령 다시 불러오기 |
| `Ctrl + C` | 실행 중인 프로그램 종료 |

파일 편집은 `gedit 파일이름`으로 메모장 같은 창을 엽니다.

### 1-3. ROS2 맛보기 - turtlesim

ROS2 프로그램은 **node** 단위로 실행되고, node끼리 **topic**으로 메시지를 주고받습니다.

Ubuntu 터미널 ①
```bash
ros2 run turtlesim turtlesim_node
```
- 성공: 파란 창에 거북이 한 마리.

Ubuntu 터미널 ② (새 창)
```bash
ros2 run turtlesim turtle_teleop_key
```
- 터미널 ②를 클릭한 상태에서 방향키를 누르면 거북이가 움직입니다.

Ubuntu 터미널 ③ (새 창)
```bash
ros2 node list
ros2 topic list
ros2 topic echo /turtle1/pose
```
- `ros2 node list`: 실행 중인 node 2개(`/turtlesim`, `/teleop_turtle`).
- `ros2 topic echo`: 거북이 위치가 계속 출력됨. `Ctrl + C`로 멈춤.

Ubuntu 터미널 ③
```bash
rqt_graph
```
- node(동그라미)와 topic(화살표)의 연결 그림이 보입니다.

**확인 질문**: 키보드 node와 거북이 node는 어떤 topic으로 연결되어 있나요?
<details><summary>답</summary>

`/turtle1/cmd_vel`
</details>

모든 터미널에서 `Ctrl + C`로 종료합니다.

---

## 2차시 - package 만들고 node 실행하기

**package** = node 코드를 담는 폴더. **workspace**(`~/ros2_ws`) 안의 `src` 폴더에 만듭니다.

### 2-1. package 생성

Ubuntu 터미널
```bash
cd ~/ros2_ws/src
ros2 pkg create my_first_pkg --build-type ament_python --dependencies rclpy std_msgs --node-name hello
```
- 성공: `my_first_pkg` 폴더가 생기고 마지막 줄에 파일 목록이 출력됨.

생긴 구조
```
my_first_pkg/
├── my_first_pkg/
│   ├── __init__.py
│   └── hello.py        ← node 코드
├── package.xml         ← package 정보, 의존성
├── setup.py            ← 실행 이름 등록
└── setup.cfg
```

### 2-2. build와 실행

Ubuntu 터미널
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_first_pkg
source install/local_setup.bash
ros2 run my_first_pkg hello
```
- 성공: `Hi from my_first_pkg.` 출력.

### 2-3. hello 고쳐보기

Ubuntu 터미널
```bash
gedit ~/ros2_ws/src/my_first_pkg/my_first_pkg/hello.py
```
`print(...)` 안의 문장을 바꾸고 저장한 뒤 다시 실행합니다.

Ubuntu 터미널
```bash
ros2 run my_first_pkg hello
```
- `--symlink-install`로 build했기 때문에 Python 파일 수정은 다시 build하지 않아도 반영됩니다. (새 파일 추가, `setup.py` 수정은 다시 build 필요)

---

## 3차시 - publisher · subscriber

talker node가 `chatter` topic으로 문장을 보내고, listener node가 받습니다.

### 3-1. talker 작성

Ubuntu 터미널
```bash
gedit ~/ros2_ws/src/my_first_pkg/my_first_pkg/talker.py
```

<!-- sync: answers/course_basics/course_basics/talker.py -->
```python
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
        msg.data = f'Hello ROS2 {self.count}'
        self.pub.publish(msg)
        self.get_logger().info(f'Sent: {msg.data}')
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
```

### 3-2. listener 작성

Ubuntu 터미널
```bash
gedit ~/ros2_ws/src/my_first_pkg/my_first_pkg/listener.py
```

<!-- sync: answers/course_basics/course_basics/listener.py -->
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(String, 'chatter', self.on_msg, 10)

    def on_msg(self, msg):  # 메시지가 도착할 때마다 실행
        self.get_logger().info(f'Received: {msg.data}')


def main():
    rclpy.init()
    node = Listener()
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

### 3-3. 실행 이름 등록 (`setup.py`)

Ubuntu 터미널
```bash
gedit ~/ros2_ws/src/my_first_pkg/setup.py
```
`entry_points` 부분을 아래처럼 바꿉니다. 형식은 `'실행이름 = package이름.파일이름:main'`.

```python
    entry_points={
        'console_scripts': [
            'hello = my_first_pkg.hello:main',
            'talker = my_first_pkg.talker:main',
            'listener = my_first_pkg.listener:main',
        ],
    },
```

### 3-4. build와 실행

Ubuntu 터미널 ①
```bash
cd ~/ros2_ws
colcon build --symlink-install --packages-select my_first_pkg
source install/local_setup.bash
ros2 run my_first_pkg talker
```

Ubuntu 터미널 ② (새 창)
```bash
ros2 run my_first_pkg listener
```
- 성공: ①에 `Sent: Hello ROS2 0, 1, 2 ...`, ②에 `Received: ...`이 같은 번호로 출력됨.

### 3-5. 명령어로 topic 다루기

Ubuntu 터미널 ③ (새 창)
```bash
ros2 topic list
ros2 topic echo /chatter
ros2 topic hz /chatter
```
- `hz`: 1초에 약 2번(0.5초 주기) 오는지 확인.

talker를 끄고(① `Ctrl + C`) 직접 메시지를 보내봅니다.

Ubuntu 터미널 ①
```bash
ros2 topic pub --once /chatter std_msgs/msg/String "{data: 'Hello from terminal'}"
```
- 성공: ② listener에 `Received: Hello from terminal`.
- ② listener가 켜져 있어야 보냅니다. listener가 없으면 `Waiting for at least 1 matching subscription(s)...`만 반복됩니다.

**확인 질문**: talker 주기를 1초로 바꾸려면 어느 줄을 고치나요?
<details><summary>답</summary>

`self.create_timer(0.5, ...)`의 `0.5`를 `1.0`으로.
</details>

## 문제 해결

| 증상 | 조치 |
|---|---|
| `Package 'my_first_pkg' not found` | `source ~/ros2_ws/install/local_setup.bash` 후 다시 실행 |
| `No executable found` | `setup.py`의 `entry_points` 확인 후 다시 build |
| listener에 아무것도 안 옴 | 두 터미널의 `echo $ROS_DOMAIN_ID`가 같은지 확인 |
| `IndentationError` | Python은 들여쓰기(공백 4칸)가 문법. 탭과 공백을 섞지 않기 |
