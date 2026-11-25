# 브라우저로 실습하기 (GitHub Codespaces)

실습실 PC에 WSL을 설치할 수 없을 때(관리자 권한 없음, 재부팅 시 복원 등) 브라우저만으로 같은 실습을 합니다. PC에는 아무것도 설치하지 않습니다.

준비물: GitHub 계정(무료, `https://github.com/signup`에서 이메일 인증 후 사용). 개인 계정은 매월 무료 사용 시간이 있습니다(4코어 기준 약 30시간). 학생마다 자기 계정을 씁니다.

## 1. Codespace 만들기

1. 브라우저에서 `https://github.com/lhc-code/ros2-gazebo-wsl-intro` 에 접속하고 로그인합니다.
2. 초록색 `Code` 버튼 → `Codespaces` 탭 → `Create codespace on main`을 누릅니다.
3. 처음 한 번은 ROS2 설치 때문에 약 5 ~ 15분 걸립니다.
- 성공: 브라우저에 VS Code 화면이 열리고, 아래 터미널에 `준비 완료.`가 표시됨.
- `Running postCreateCommand` 앞에 빨간 `✕`가 보이면 VS Code 터미널에서 `bash .devcontainer/post_create.sh`를 실행합니다.

## 2. 데스크톱 화면 열기

GUI 창(turtlesim, RViz, Gazebo)은 별도 데스크톱 화면에 뜹니다.

1. VS Code 아래쪽 `포트`(PORTS) 탭에서 `6080` 줄의 지구본 아이콘을 누릅니다.
2. VS Code 안에 "간단한 브라우저"가 열리면 화면이 깨져 보입니다. 주소창 오른쪽 끝 `↗` 아이콘을 눌러 크롬 새 탭으로 엽니다.
3. 새 탭에서 `Connect`를 누르고 비밀번호 `ros2`를 입력합니다.
- 성공: 탭 제목이 `fluxbox - noVNC`로 바뀌고 빈 데스크톱이 보임.
- 화면이 잘리면 왼쪽 noVNC 메뉴의 설정(톱니바퀴) → `Scaling Mode`를 `Remote Resizing`으로 바꿉니다.

## 3. 실행 확인

설치 후에는 VS Code 터미널 오른쪽 위 `+`로 새 터미널을 엽니다. 설치 전에 열려 있던 터미널에서는 `ros2: command not found`가 나오므로 `source ~/.bashrc`를 먼저 실행합니다.

VS Code 터미널
```bash
ros2 run turtlesim turtlesim_node
```
- 성공: noVNC 탭에 파란 배경의 `TurtleSim` 창과 거북이가 뜸.

이후 실습은 `practice/` 가이드를 그대로 따릅니다. "Ubuntu 터미널"은 VS Code 터미널로 바꿔 읽습니다. 경로 `~/ros2_ws/src/ros2-gazebo-wsl-intro`도 그대로 쓸 수 있습니다.

## 주의

- 수업이 끝나면 `https://github.com/codespaces`에서 Codespace를 `Stop` 또는 `Delete`합니다. 켜 두면 무료 시간이 줄어듭니다.
- 30분 동안 입력이 없으면 자동으로 멈춥니다. 다시 열면 작업 파일은 남아 있습니다.
- Gazebo는 CPU 렌더링이라 느릴 수 있습니다. [미검증]
