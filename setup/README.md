# 환경 설치 (WSL2 + Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic)

설치는 수업 전에 끝내 두는 것을 권장합니다. 전체 약 30 ~ 60분(인터넷 속도에 따라 다름).

## 1. WSL2와 Ubuntu 24.04 설치

Windows PowerShell (관리자 권한으로 실행)
```powershell
wsl --install -d Ubuntu-24.04
```
- 설치가 끝나면 PC를 재부팅합니다.
- 재부팅 후 Ubuntu 창이 뜨면 사용자 이름과 비밀번호를 정합니다. 비밀번호는 입력해도 화면에 표시되지 않습니다.
- 설치가 `0.0%`에서 멈추면(학교망 등) [학교망 설치 방법](school_network.md)을 따릅니다.
- 관리자 권한이 없어 WSL을 설치할 수 없으면 [브라우저로 실습하기](codespaces.md)를 따릅니다.

Windows PowerShell
```powershell
wsl --update
wsl -l -v
```
- 성공: `Ubuntu-24.04`의 `VERSION`이 `2`로 표시됨.

### (선택) WSL 메모리 늘리기

WSL은 기본으로 PC 메모리의 절반만 씁니다. RAM 8GB PC에서 Gazebo가 느리면 Windows 쪽 `C:\Users\<사용자>\.wslconfig` 파일에 메모리와 swap(메모리가 모자랄 때 디스크를 임시 메모리로 쓰는 공간) 크기를 적습니다.

Ubuntu 터미널
```bash
free -h
```
- 현재 값: `Mem`의 `total`이 WSL 메모리, `Swap`의 `total`이 swap 크기입니다. RAM 8GB PC에서는 보통 `3.7Gi`, `1.0Gi`로 나옵니다.

Ubuntu 터미널
```bash
ls /mnt/c/Users/
```
- 목록에서 자신의 Windows 사용자 이름을 확인합니다. 아래 명령의 `kime`를 그 이름으로 바꿉니다.

Ubuntu 터미널
```bash
printf "[wsl2]\nmemory=6GB\nswap=4GB\n" > /mnt/c/Users/kime/.wslconfig
cat /mnt/c/Users/kime/.wslconfig
```
- 성공: `[wsl2]`, `memory=6GB`, `swap=4GB` 세 줄이 출력됨.
- `memory=6GB` 같은 줄을 터미널에 직접 입력하면 설정되지 않습니다. 반드시 위 명령으로 파일에 씁니다.

Windows PowerShell
```powershell
wsl --shutdown
```
- 열려 있던 Ubuntu 창은 닫고 새로 엽니다. Ubuntu 안에서 `wsl.exe --shutdown`을 실행하면 창에 깨진 문자가 나올 수 있는데, 창을 닫으면 됩니다.

Ubuntu 터미널
```bash
free -h
```
- 성공: `Mem` total 약 `5.8Gi`, `Swap` total `4.0Gi`.
- Windows가 느려지면 `memory=5GB`로 낮춥니다.

## 2. ROS2 Jazzy + Gazebo Harmonic 설치

Ubuntu 터미널
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/lhc-code/ros2-gazebo-wsl-intro.git
bash ros2-gazebo-wsl-intro/setup/install_ros2_jazzy.sh 1
```
- 마지막 숫자 `1`은 **자리 번호(1 ~ 20)** 입니다. 옆 자리와 ROS2 통신이 섞이지 않도록 자리마다 다른 번호를 씁니다(`ROS_DOMAIN_ID`).
- 중간에 비밀번호를 물으면 1단계에서 정한 비밀번호를 입력합니다.

설치가 끝나면 터미널을 닫고 새로 엽니다.

## 3. 진단

Ubuntu 터미널
```bash
bash ~/ros2_ws/src/ros2-gazebo-wsl-intro/setup/check_env.sh
```
- 성공: 모든 줄이 `[OK]` 또는 `[주의]`. `[실패]`가 있으면 아래 표를 봅니다.

## 문제 해결

| 증상 | 원인 | 조치 |
|---|---|---|
| `wsl --install` 후 "가상화를 사용할 수 없음" | BIOS에서 가상화(VT-x/SVM) 꺼짐 | BIOS에서 가상화 켜기 (실습실 관리자 확인 필요) |
| `wsl -l -v`에서 VERSION이 1 | WSL1로 설치됨 | `wsl --set-version Ubuntu-24.04 2` |
| `wsl --install`이 `0.0%`에서 멈춤 | 네트워크에서 Microsoft Store 다운로드 차단 | [학교망 설치 방법](school_network.md) |
| Ubuntu 안에서 `wsl: command not found` | `wsl`은 Windows 명령 | `wsl.exe -l -v`로 입력하거나 PowerShell에서 실행 |
| `ros2: command not found` | ROS2 미설치, 또는 새 터미널을 열지 않음 | `ls /opt/ros/`에 `jazzy`가 없으면 2단계 실행. 있으면 터미널을 다시 열거나 `source ~/.bashrc` |
| Gazebo 창이 검은 화면 / 바로 꺼짐 | CPU 렌더링에서 ogre2 문제 | `ros2 launch course_robot gazebo.launch.py render_engine:=ogre` [미검증] |
| Gazebo 창은 뜨는데 로봇이 안 보임 | GUI와 서버 연결 실패 | `export GZ_IP=127.0.0.1` 후 다시 실행 [미검증] |
| 옆 자리 topic이 보임 | `ROS_DOMAIN_ID` 같음 | `~/.bashrc`의 `ROS_DOMAIN_ID` 숫자 변경 |
| GUI 창(RViz, turtlesim)이 안 뜸 | WSLg 미동작 | PowerShell에서 `wsl --update` 후 `wsl --shutdown` |
