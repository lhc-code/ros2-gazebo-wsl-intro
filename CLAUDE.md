# CLAUDE.md

고등학생 대상 ROS2·Gazebo 입문 단기과정 실습 저장소. 학생 배포 자료는 `practice/`, 정답 코드는 `answers/`, 환경 설치는 `setup/`, 준비·내부 메모는 `archive/`에 둔다.

## 과정 기본 정보

| 항목 | 값 |
|---|---|
| 대상 | 공업고등학교 학생 20명, 로봇·프로그래밍 입문자 |
| 환경 | 실습실 Windows 10/11 PC → WSL2 + Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic |
| 렌더링 | GPU 없음, CPU(llvmpipe) 렌더링 전제 |
| 일정 | 1일차 견학·이론 / 2일차 오전 3차시 / 3일차 6차시 / 4일차 현장실습 (1차시 = 50분) |

## 작성 규칙 - 문체

- 독자는 고등학생 입문자다. 학생용 문서(`practice/`, `setup/`)는 "~합니다" 경어체로 짧게 쓴다.
- 이모지, 느낌표 남발, "쉽죠?" 같은 표현을 쓰지 않는다. 대신 명령어마다 "무엇이 보이면 성공인지"를 적는다.
- 명령어는 반드시 코드 블록에 두고, 한 블록에는 한 번에 붙여넣을 명령만 둔다. 실행 위치(Windows PowerShell / Ubuntu 터미널)를 블록 위에 적는다.
- ROS2 용어는 영어 원문을 쓴다: node, topic, service, parameter, launch, package, workspace, publisher, subscriber.
- 범위 표기 `~`는 앞뒤를 띄어 쓴다("1 ~ 3차시"). 붙여 쓰면 GitHub 마크다운에서 취소선이 됨.
- 외부 상용 강의의 이름·코드·문구를 넣지 않는다. 코드는 이 저장소에서 새로 작성한 것만 쓴다.
- 개인 연락처(전화번호, 개인 메일)를 공개 파일에 넣지 않는다.

## 작성 규칙 - 코드

- ROS2 Jazzy, Python(`rclpy`), `ament_python`만 쓴다. C++·커스텀 msg/srv는 쓰지 않는다(빌드 시간과 오류 지점을 줄이기 위함).
- service는 `example_interfaces/srv/AddTwoInts`를 쓴다.
- Gazebo는 Harmonic(`gz sim`)과 `ros_gz_sim`, `ros_gz_bridge`를 쓴다. Gazebo Classic(`gazebo_ros`) 문법을 섞지 않는다.
- 학생 실습 노드는 50줄 안팎으로 유지하고, 주석은 학생이 따라 칠 때 필요한 한 줄 설명만 단다.
- `answers/`의 코드와 `practice/*.md` 본문의 코드는 항상 같아야 한다. 가이드 코드 블록 위에 `<!-- sync: answers/경로 -->`를 달고, 고친 뒤 `python3 archive/check_code_sync.py`로 확인한다.

## 작업 방식

- 변경은 작업 브랜치에 commit·push한 뒤 PR을 만들어 main에 merge하는 것을 기본으로 한다.
- 실기 검증(WSL 실습실 PC에서 실제 실행)을 하지 않은 내용은 문서에 `[미검증]`으로 표시하고, 검증 후 지운다.
- 실행 결과(터미널 출력, 오류 메시지)를 받으면 가이드의 "성공 화면"과 문제 해결 표를 실제 결과에 맞춘다.
- "남은 작업 확인" 요청 시 점검 항목:
  1. `answers/` ↔ `practice/*.md` 코드 일치
  2. `[미검증]` 표시 남은 곳
  3. 차시 표(`.github/README.md`, `practice/README.md`)와 강의계획서 일치
  4. `~` 띄어쓰기, 개인정보, 외부 강의 흔적
  5. CI(`.github/workflows/build.yml`) 통과 여부
