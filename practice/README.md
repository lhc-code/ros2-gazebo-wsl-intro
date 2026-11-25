# practice

학생용 차시별 실습 가이드. 차시 순서대로 진행합니다.

| 파일 | 일차 | 내용 |
|---|---|---|
| [day1_slides/](day1_slides/) | 1일차 (화) | 이론 슬라이드 (트렌드 · 디지털 트윈 · 진로) |
| [day2_wed.md](day2_wed.md) | 2일차 (수, 오전 3차시) | 터미널 · ROS2 소개 → package 생성 → publisher · subscriber |
| [day3_thu.md](day3_thu.md) | 3일차 (목, 6차시) | service → parameter · launch → turtlesim → URDF → Gazebo → 1m 이동 |
| [extra_turtlebot3_slam_nav.md](extra_turtlebot3_slam_nav.md) | 번외 | TurtleBot3 SLAM 지도 만들기 → Nav2 자율주행 `[미검증]` |
| `docs/image/` | - | 가이드에 쓰는 캡처 |

## 공통 약속

- **Windows PowerShell** / **Ubuntu 터미널** 표시를 보고 해당 창에 입력합니다.
- 새 터미널을 열 때마다 아래 명령은 자동으로 실행됩니다(`~/.bashrc`). 직접 칠 필요 없습니다.
  ```bash
  source /opt/ros/jazzy/setup.bash
  source ~/ros2_ws/install/local_setup.bash
  ```
- 코드를 고친 뒤에는 항상 **build → source → run** 순서입니다.
  ```bash
  cd ~/ros2_ws && colcon build --symlink-install && source install/local_setup.bash
  ```
- 실행 중인 프로그램은 `Ctrl + C`로 끕니다.
- 막히면 `answers/`의 같은 이름 파일과 비교합니다.
