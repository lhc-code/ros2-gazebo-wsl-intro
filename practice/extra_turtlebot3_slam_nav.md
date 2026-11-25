# 번외 - TurtleBot3로 지도 만들기(SLAM)와 자율주행(Nav2) [미검증]

정규 차시가 끝난 뒤 시간이 남거나, 더 해보고 싶은 사람을 위한 과제입니다. 전체 내용이 실기 검증 전입니다(`[미검증]`).

흐름: 설치 → Gazebo 월드 → SLAM → 키보드로 돌아다니며 지도 그리기 → 지도 저장 → 저장한 지도로 자율주행

- 환경: [setup/README.md](../setup/README.md)로 ROS2 Jazzy + Gazebo Harmonic 설치가 끝난 상태
- 메모리: Gazebo + SLAM + Nav2 + RViz를 동시에 띄우므로 `setup/README.md`의 `.wslconfig`(메모리 6GB) 설정을 권장합니다.
- 공식 문서: `https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/`

---

## 1. 설치 (1회, 약 20 ~ 30분)

SLAM(Cartographer)과 자율주행(Nav2) 패키지를 설치합니다.

Ubuntu 터미널
```bash
sudo apt install -y ros-jazzy-cartographer ros-jazzy-cartographer-ros ros-jazzy-navigation2 ros-jazzy-nav2-bringup
```
- 성공: 마지막에 오류 없이 프롬프트로 돌아옴.

TurtleBot3 package를 내려받아 build합니다. 이 저장소의 `~/ros2_ws`와 섞이지 않도록 별도 workspace `~/turtlebot3_ws`를 씁니다.

Ubuntu 터미널
```bash
mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
git clone -b jazzy https://github.com/ROBOTIS-GIT/DynamixelSDK.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b jazzy https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
```

Ubuntu 터미널
```bash
cd ~/turtlebot3_ws && colcon build --symlink-install
```
- 성공: `Summary: N packages finished`가 나오고 `failed`가 없음.

Ubuntu 터미널
```bash
echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```
- 공식 문서의 `ROS_DOMAIN_ID=30` 설정은 실물 로봇 연결용이라 시뮬레이션에서는 하지 않습니다.

## 2. 지도 만들기 (SLAM)

터미널 3개를 씁니다.

Ubuntu 터미널 ① - Gazebo 월드
```bash
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```
- 성공: Gazebo 창에 기둥이 있는 육각형 월드와 작은 로봇이 보임. CPU 렌더링이라 1분 정도 걸릴 수 있습니다.

Ubuntu 터미널 ② - SLAM (RViz가 함께 뜸)
```bash
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```
- 성공: RViz 창에 로봇 주변 지도가 회색·검은색으로 그려지기 시작함.

Ubuntu 터미널 ③ - 키보드 조종
```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

| 키 | 동작 |
|---|---|
| `w` / `x` | 전진 속도 올리기 / 내리기 |
| `a` / `d` | 회전 속도 왼쪽 / 오른쪽 |
| `s` | 정지 |

- 터미널 ③을 클릭한 상태에서 눌러야 합니다.
- 천천히 월드 전체를 한 바퀴 돕니다. 빨리 돌면 지도가 틀어집니다.
- 성공: RViz의 지도에서 벽과 기둥이 검은 선으로 닫힌 모양이 됨.

## 3. 지도 저장

Ubuntu 터미널 ④ (새 창)
```bash
ros2 run nav2_map_server map_saver_cli -f ~/map
```
- 성공: 홈 폴더에 `map.pgm`(그림), `map.yaml`(설정) 두 파일이 생김. `ls ~/map.*`로 확인합니다.

저장이 끝나면 ②, ③은 `Ctrl + C`로 끕니다. ① Gazebo는 그대로 둡니다.

## 4. 자율주행 (Nav2)

Ubuntu 터미널 ②
```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map.yaml
```
- 성공: RViz에 저장한 지도가 뜸.

RViz에서 순서대로 누릅니다.

1. **2D Pose Estimate** → Gazebo에서 로봇이 있는 위치를 지도에서 클릭하고, 로봇이 보는 방향으로 드래그합니다.
2. **Nav2 Goal** → 가고 싶은 지점을 클릭하고 도착 방향으로 드래그합니다.

- 성공: 로봇이 경로(초록 선)를 만들고 장애물을 피해 목표까지 스스로 이동함.

## 문제 해결

| 증상 | 조치 |
|---|---|
| `Package 'turtlebot3_gazebo' not found` | `source ~/.bashrc` 후 다시 실행. 그래도 없으면 1단계 build 결과 확인 |
| `KeyError: 'TURTLEBOT3_MODEL'` | `export TURTLEBOT3_MODEL=burger` 후 다시 실행 |
| RViz에 지도가 안 그려짐 | ② 명령에 `use_sim_time:=True`가 있는지 확인 |
| 모든 창이 매우 느림 | 다른 프로그램 종료, `.wslconfig` 메모리 늘리기, Gazebo 창 최소화 |
| Nav2 Goal을 찍어도 안 움직임 | 먼저 2D Pose Estimate로 위치를 맞췄는지 확인 |
