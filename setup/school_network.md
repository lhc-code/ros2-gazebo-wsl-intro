# WSL 설치 - 학교망에서 다운로드가 멈출 때

[환경 설치](README.md) 1단계의 `wsl --install`이 `0.0%`에서 멈출 때만 이 페이지를 봅니다. 일반 환경에서는 [README.md](README.md)의 순서를 따릅니다.

실습실 PC(Windows 10 22H2, 빌드 19045, 2026-11-24)에서 확인한 순서입니다. 학교망에서는 Microsoft Store 경유 다운로드가 막히므로 `--web-download`를 붙여 GitHub·Ubuntu 서버에서 직접 받습니다.

## 1. WSL 기능 켜기

멈춘 명령은 `Ctrl+C`로 끊습니다.

Windows PowerShell (관리자 권한으로 실행)
```powershell
wsl --install -d Ubuntu-24.04 --web-download
```
- 성공: `Microsoft-Windows-Subsystem-Linux`, `VirtualMachinePlatform` 두 항목이 각각 `100.0%`까지 진행되고 마지막에 "요청한 작업이 잘 실행되었습니다. 시스템을 다시 시작하면 변경 사항이 적용됩니다."가 표시됨.
- 옵션 이름은 `--web-download`입니다. `--web-downloads`처럼 s를 붙이면 `Wsl/E_INVALIDARG` 오류가 납니다.

PC를 재부팅합니다.

## 2. Ubuntu 24.04 설치

Windows PowerShell (관리자 권한으로 실행)
```powershell
wsl --install -d Ubuntu-24.04 --web-download
```
- 성공: "다운로드 중: Ubuntu 24.04 LTS" → "설치 중: Ubuntu 24.04 LTS" → "배포가 설치되었습니다."가 표시되고, 이어서 `Create a default Unix user account:`가 나옴.
- 사용자 이름과 비밀번호를 정합니다. 비밀번호는 입력해도 화면에 표시되지 않습니다.
- 성공: `passwd: password updated successfully`가 표시되고 프롬프트가 `사용자@PC이름:~$` 형태로 바뀜.

## 3. 확인

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

여기까지 되면 [README.md](README.md)의 2단계(ROS2 Jazzy + Gazebo Harmonic 설치)로 돌아갑니다.

## 4. (대안) Ubuntu 다운로드도 막힐 때 USB로 설치 [미검증]

2단계가 재부팅 후에도 `0.0%`에서 멈추면 다른 PC에서 이미지를 받아 USB로 옮깁니다.

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

## 문제 해결

| 증상 | 원인 | 조치 |
|---|---|---|
| "설치 중: Linux용 Windows 하위 시스템 0.0%"에서 멈춤 | 학교망에서 Microsoft Store 다운로드 차단 | `Ctrl+C` → 1단계 |
| "설치 중: Ubuntu 0.0%"에서 멈춤 | WSL 기능이 아직 켜지지 않음(재부팅 전) | `Ctrl+C` → 1단계 → 재부팅 → 2단계 |
| 재부팅 후에도 Ubuntu 다운로드가 `0.0%` | 학교망에서 Ubuntu 이미지 다운로드 차단 | 4단계(USB 설치) [미검증] |
| `Wsl/E_INVALIDARG` | 옵션 오타(`--web-downloads` 등) | `--web-download`로 다시 입력 |
| 재부팅하면 설치한 WSL·Ubuntu가 사라짐 | 실습실 PC 복원 프로그램 동작 | 실습실 관리자에게 복원 해제 요청 [미검증] |
