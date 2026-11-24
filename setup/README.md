# 환경 설치 (WSL2 + Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic)

설치는 수업 전에 끝내 두는 것을 권장합니다. 전체 약 30 ~ 60분(인터넷 속도에 따라 다름).

## 1. WSL2와 Ubuntu 24.04 설치

실습실 PC(Windows 10 22H2, 빌드 19045)에서 확인한 순서입니다. 학교망에서는 Microsoft Store 경유 다운로드가 `0.0%`에서 멈추므로 처음부터 `--web-download`를 붙입니다.

### 1-1. WSL 기능 켜기

Windows PowerShell (관리자 권한으로 실행)
```powershell
wsl --install -d Ubuntu-24.04 --web-download
```
- 성공: `Microsoft-Windows-Subsystem-Linux`, `VirtualMachinePlatform` 두 항목이 각각 `100.0%`까지 진행되고 마지막에 "요청한 작업이 잘 실행되었습니다. 시스템을 다시 시작하면 변경 사항이 적용됩니다."가 표시됨.
- 옵션 이름은 `--web-download`입니다. `--web-downloads`처럼 s를 붙이면 `Wsl/E_INVALIDARG` 오류가 납니다.

PC를 재부팅합니다.

### 1-2. Ubuntu 24.04 설치

Windows PowerShell (관리자 권한으로 실행)
```powershell
wsl --install -d Ubuntu-24.04 --web-download
```
- 성공: "다운로드 중: Ubuntu 24.04 LTS" → "설치 중: Ubuntu 24.04 LTS" → "배포가 설치되었습니다."가 표시되고, 이어서 `Create a default Unix user account:`가 나옴.
- 사용자 이름과 비밀번호를 정합니다. 비밀번호는 입력해도 화면에 표시되지 않습니다.
- 성공: `passwd: password updated successfully`가 표시되고 프롬프트가 `사용자@PC이름:~$` 형태로 바뀜.

### 1-3. 확인

Ubuntu 터미널
```bash
cd ~
wsl.exe -l -v
```
- 성공: `Ubuntu-24.04`의 `VERSION`이 `2`로 표시됨.
- Ubuntu 안에서는 `wsl`이 아니라 `wsl.exe`로 입력합니다. `wsl`만 치면 `wsl: command not found`가 나옵니다.
- 처음 열린 위치는 `/mnt/c/Users/...`(Windows 폴더)이므로 `cd ~`로 Ubuntu 홈으로 이동합니다.

Ubuntu 터미널
```bash
lsb_release -a
```
- 성공: `Ubuntu 24.04.x LTS`, `Codename: noble`이 표시됨.

Ubuntu 터미널
```bash
sudo apt update
```
- 성공: `Get:... http://archive.ubuntu.com/ubuntu noble ...` 줄이 이어지다가 `Reading package lists... Done`으로 끝남. 학교망에서 apt가 열려 있다는 뜻입니다.

### 1-4. (대안) 학교망에서 Ubuntu 다운로드가 막힐 때 USB로 설치 [미검증]

1-2 단계가 `0.0%`에서 계속 멈추면 다른 PC에서 이미지를 받아 USB로 옮깁니다.

1. 다른 PC에서 `https://releases.ubuntu.com/noble/`에 접속해 WSL 이미지(`ubuntu-24.04.x-wsl-amd64.wsl`, 약 350MB)를 받아 USB에 복사합니다.
2. 실습실 PC에서 아래 명령을 실행합니다. `D:`는 USB 드라이브 문자에 맞게 바꿉니다.

Windows PowerShell (관리자 권한으로 실행)
```powershell
wsl --install --from-file D:\ubuntu-24.04.3-wsl-amd64.wsl
```
- 성공: 사용자 이름 입력 화면이 나옴.

위 명령이 오류를 내면(WSL 2.4.8 미만) import로 설치합니다.

Windows PowerShell (관리자 권한으로 실행)
```powershell
mkdir C:\WSL\Ubuntu
wsl --import Ubuntu-24.04 C:\WSL\Ubuntu D:\ubuntu-24.04.3-wsl-amd64.wsl
wsl -d Ubuntu-24.04
```
- 성공: `root@PC이름:~#` 프롬프트가 나옴. import 방식은 root로 들어가므로 `adduser 사용자이름`으로 사용자를 만듭니다.

### (선택) WSL 메모리 늘리기

WSL은 기본으로 PC 메모리의 절반만 씁니다. RAM 8GB PC에서 Gazebo가 느리면 `C:\Users\<사용자>\.wslconfig` 파일을 만들고 아래 내용을 넣은 뒤 `wsl --shutdown`으로 재시작합니다.

```ini
[wsl2]
memory=6GB
swap=4GB
```

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
| `wsl --install`이 "설치 중: Linux용 Windows 하위 시스템 0.0%"에서 멈춤 | 학교망에서 Microsoft Store 다운로드 차단 | `Ctrl+C`로 끊고 `wsl --install -d Ubuntu-24.04 --web-download` |
| "설치 중: Ubuntu 0.0%"에서 멈춤 | WSL 기능이 아직 켜지지 않음(재부팅 전) | `Ctrl+C` → 1-1 단계 실행 → 재부팅 → 1-2 단계 |
| 재부팅 후에도 Ubuntu 다운로드가 `0.0%` | 학교망에서 Ubuntu 이미지 다운로드 차단 | 1-4 단계(USB 설치) [미검증] |
| `Wsl/E_INVALIDARG` | 옵션 오타(`--web-downloads` 등) | `--web-download`로 다시 입력 |
| Ubuntu 안에서 `wsl: command not found` | `wsl`은 Windows 명령 | `wsl.exe -l -v`로 입력하거나 PowerShell에서 실행 |
| 재부팅하면 설치한 WSL·Ubuntu가 사라짐 | 실습실 PC 복원 프로그램 동작 | 실습실 관리자에게 복원 해제 요청 [미검증] |
| `wsl --install` 후 "가상화를 사용할 수 없음" | BIOS에서 가상화(VT-x/SVM) 꺼짐 | BIOS에서 가상화 켜기 (실습실 관리자 확인 필요) |
| `wsl -l -v`에서 VERSION이 1 | WSL1로 설치됨 | `wsl --set-version Ubuntu-24.04 2` |
| `ros2: command not found` | ROS2 미설치, 또는 새 터미널을 열지 않음 | `ls /opt/ros/`에 `jazzy`가 없으면 2단계 실행. 있으면 터미널을 다시 열거나 `source /opt/ros/jazzy/setup.bash` |
| Gazebo 창이 검은 화면 / 바로 꺼짐 | CPU 렌더링에서 ogre2 문제 | `ros2 launch course_robot gazebo.launch.py render_engine:=ogre` [미검증] |
| Gazebo 창은 뜨는데 로봇이 안 보임 | GUI와 서버 연결 실패 | `export GZ_IP=127.0.0.1` 후 다시 실행 [미검증] |
| 옆 자리 topic이 보임 | `ROS_DOMAIN_ID` 같음 | `~/.bashrc`의 `ROS_DOMAIN_ID` 숫자 변경 |
| GUI 창(RViz, turtlesim)이 안 뜸 | WSLg 미동작 | PowerShell에서 `wsl --update` 후 `wsl --shutdown` |
