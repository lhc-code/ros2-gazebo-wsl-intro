#!/usr/bin/env bash
# ROS2 Jazzy + Gazebo Harmonic 설치 (Ubuntu 24.04 / WSL2)
# 사용법: bash install_ros2_jazzy.sh <자리번호 1~20>
set -euo pipefail

SEAT="${1:-}"
if ! [[ "$SEAT" =~ ^[0-9]+$ ]] || (( SEAT < 1 || SEAT > 101 )); then
  echo "사용법: bash install_ros2_jazzy.sh <자리번호 1~20>"
  exit 1
fi

. /etc/os-release
if [[ "${VERSION_CODENAME}" != "noble" ]]; then
  echo "[실패] Ubuntu 24.04(noble)가 아닙니다: ${PRETTY_NAME}"
  exit 1
fi

echo "== 1/4 기본 도구 =="
sudo apt-get update
sudo apt-get install -y software-properties-common curl git locales
sudo add-apt-repository -y universe
sudo locale-gen en_US.UTF-8

echo "== 2/4 ROS2 apt 저장소 =="
if ! dpkg -s ros2-apt-source >/dev/null 2>&1; then
  # 최신 릴리스 페이지로 리다이렉트되는 주소에서 버전만 추출 (GitHub API 요청 제한 회피)
  VER=$(curl -fsSL -o /dev/null -w '%{url_effective}' \
        https://github.com/ros-infrastructure/ros-apt-source/releases/latest | sed 's#.*/tag/##')
  if [[ -z "${VER}" || "${VER}" == http* ]]; then
    echo "[실패] ros-apt-source 버전을 찾지 못했습니다. github.com 접속을 확인하세요."
    exit 1
  fi
  echo "ros-apt-source ${VER}"
  curl -L -o /tmp/ros2-apt-source.deb \
    "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${VER}/ros2-apt-source_${VER}.${VERSION_CODENAME}_all.deb"
  sudo dpkg -i /tmp/ros2-apt-source.deb
fi
sudo apt-get update

echo "== 3/4 ROS2 Jazzy + Gazebo Harmonic 패키지 =="
# ros-jazzy-ros-gz 가 Jazzy 짝 버전인 Gazebo Harmonic을 함께 설치함
sudo apt-get install -y \
  ros-jazzy-desktop \
  ros-jazzy-ros-gz \
  ros-jazzy-xacro \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-teleop-twist-keyboard \
  python3-colcon-common-extensions \
  python3-rosdep \
  mesa-utils \
  gedit

if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
  sudo rosdep init
fi
rosdep update

echo "== 4/4 ~/.bashrc 환경 설정 =="
MARK_BEGIN="# >>> ros2-course >>>"
MARK_END="# <<< ros2-course <<<"
# 이전 블록이 있으면 지우고 다시 씀 (자리 번호 변경 대비)
sed -i "/${MARK_BEGIN}/,/${MARK_END}/d" ~/.bashrc
cat >> ~/.bashrc <<EOF
${MARK_BEGIN}
source /opt/ros/jazzy/setup.bash
[ -f ~/ros2_ws/install/local_setup.bash ] && source ~/ros2_ws/install/local_setup.bash
export ROS_DOMAIN_ID=${SEAT}
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
${MARK_END}
EOF

echo
echo "설치 완료. 터미널을 닫고 새로 연 뒤 진단 스크립트를 실행하세요:"
echo "  bash ~/ros2_ws/src/ros2-gazebo-wsl-intro/setup/check_env.sh"
