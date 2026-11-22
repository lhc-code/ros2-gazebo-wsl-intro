# ROS2 기반 로봇 소프트웨어·시뮬레이션 입문

Windows 실습실 PC에서 **WSL2 + Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic**으로 ROS2 통신 구조와 이동 로봇 시뮬레이션을 실습하는 단기과정 자료입니다. GPU 없이 CPU 렌더링으로 진행합니다.

## 한눈에 보기

| 항목 | 내용 |
|---|---|
| 대상 | 로봇·프로그래밍 입문 고등학생 (선수지식 없음) |
| 목표 | ① ROS2 node·topic·service 이해와 구현 ② Gazebo 이동 로봇 제어 |
| 환경 | Windows 10/11, RAM 8GB 이상, WSL2 + Ubuntu 24.04 |
| 소프트웨어 | ROS2 Jazzy, Gazebo Harmonic, Python(`rclpy`) |
| 1차시 | 50분 |

## 일정

| 일차 | 차시 | 내용 | 자료 |
|---|---|---|---|
| 1일차 (화) | 1 ~ 3 | 대학 연구실 견학 | - |
| | 4 ~ 6 | 로보틱스 트렌드 · 시뮬레이션과 디지털 트윈 · 진로 (이론) | [day1_slides](../practice/day1_slides/) |
| 2일차 (수, 오전) | 1 | WSL Ubuntu 터미널 & ROS2 소개 | [day2_wed.md](../practice/day2_wed.md) |
| | 2 | ROS2 package 생성 및 node 실행 | |
| | 3 | publisher · subscriber 작성 | |
| 3일차 (목) | 1 | service server · client 작성 | [day3_thu.md](../practice/day3_thu.md) |
| | 2 | parameter · launch 파일 작성 | |
| | 3 | Turtlesim 거북이 목표점 이동 | |
| | 4 | URDF 로봇 모델 작성 및 RViz 확인 | |
| | 5 | Gazebo에 로봇 불러오기 및 키보드 주행 | |
| | 6 | Gazebo 로봇 1m 이동 node 작성 및 정리 | |
| 4일차 (금) | - | 현장실습 | - |

## 시작하기

1. [setup/README.md](../setup/README.md) 순서대로 WSL과 ROS2를 설치합니다.
2. 진단 스크립트로 환경을 확인합니다.

   Ubuntu 터미널
   ```bash
   bash ~/ros2_ws/src/ros2-gazebo-wsl-intro/setup/check_env.sh
   ```
3. [practice/](../practice/) 가이드를 차시 순서대로 따라갑니다. 막히면 [answers/](../answers/)의 정답 코드를 봅니다.

## 저장소 구성

```
setup/               설치 안내 · 설치 스크립트 · 진단 스크립트
practice/            학생용 차시별 실습 가이드
  day1_slides/       1일차 이론 슬라이드
  day2_wed.md        2일차 (수, 오전 3차시)
  day3_thu.md        3일차 (목, 6차시)
answers/             정답 package (colcon으로 바로 빌드)
  course_basics/     talker · listener · service · parameter · turtle_goal
  course_robot/      URDF · Gazebo world · launch · move_1m
archive/             강의 준비 메모
CLAUDE.md            Claude와 협업할 때의 작성 규칙
```

## 정답 코드 빌드

Ubuntu 터미널
```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/local_setup.bash
ros2 launch course_robot gazebo.launch.py
```

## Claude와 협업하기

이 저장소는 Claude(Claude Code 등)와 함께 고치는 것을 전제로 합니다. 작성 규칙과 점검 항목은 [CLAUDE.md](../CLAUDE.md)에 있습니다. 예시 요청:

- "3일차 4차시 URDF에 바퀴 하나 더 추가한 버전 만들어줘"
- "실습실 PC에서 이 오류가 났어: (오류 붙여넣기)" → 가이드의 문제 해결 표까지 갱신
- "남은 작업 확인"

## 라이선스

MIT. 동아대학교 기계공학과 KIME Lab.
