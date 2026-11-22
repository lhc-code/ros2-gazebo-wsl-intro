#!/usr/bin/env bash
# 실습 환경 진단: WSL2 / Ubuntu 24.04 / 메모리 / ROS2 Jazzy / Gazebo / GUI / 렌더러
# 사용법: bash check_env.sh

FAIL=0
ok()   { echo "[OK]   $*"; }
warn() { echo "[주의] $*"; }
bad()  { echo "[실패] $*"; FAIL=$((FAIL + 1)); }

# 1. WSL2
if grep -qi microsoft /proc/version; then
  if grep -qi "WSL2" /proc/version || [[ -d /run/WSL ]]; then ok "WSL2"; else warn "WSL 버전 확인 필요 (PowerShell: wsl -l -v)"; fi
else
  warn "WSL이 아님 (일반 Ubuntu에서도 실습은 가능)"
fi

# 2. Ubuntu 24.04
. /etc/os-release
if [[ "${VERSION_CODENAME}" == "noble" ]]; then ok "${PRETTY_NAME}"; else bad "Ubuntu 24.04 아님: ${PRETTY_NAME}"; fi

# 3. 메모리 (WSL에 할당된 양)
MEM_GB=$(awk '/MemTotal/ {printf "%.1f", $2/1024/1024}' /proc/meminfo)
if awk "BEGIN{exit !(${MEM_GB} >= 5.5)}"; then ok "메모리 ${MEM_GB}GB"
elif awk "BEGIN{exit !(${MEM_GB} >= 3.5)}"; then warn "메모리 ${MEM_GB}GB - Gazebo가 느릴 수 있음 (setup/README.md의 .wslconfig 참고)"
else bad "메모리 ${MEM_GB}GB - 부족"; fi

# 4. 디스크 여유
DISK_GB=$(df -BG --output=avail ~ | tail -1 | tr -dc '0-9')
if (( DISK_GB >= 5 )); then ok "디스크 여유 ${DISK_GB}GB"; else bad "디스크 여유 ${DISK_GB}GB - 5GB 이상 필요"; fi

# 5. ROS2 Jazzy
if [[ -f /opt/ros/jazzy/setup.bash ]]; then
  # shellcheck disable=SC1091
  source /opt/ros/jazzy/setup.bash
  ok "ROS2 Jazzy 설치됨"
else
  bad "ROS2 Jazzy 없음 - install_ros2_jazzy.sh 실행"
fi

for pkg in turtlesim ros_gz_sim ros_gz_bridge xacro teleop_twist_keyboard joint_state_publisher_gui example_interfaces; do
  if ros2 pkg prefix "$pkg" >/dev/null 2>&1; then ok "package ${pkg}"; else bad "package ${pkg} 없음"; fi
done

# 6. Gazebo
if command -v gz >/dev/null 2>&1 && gz sim --versions >/dev/null 2>&1; then
  ok "Gazebo $(gz sim --versions | head -1)"
else
  bad "Gazebo(gz sim) 없음"
fi

# 7. colcon
if command -v colcon >/dev/null 2>&1; then ok "colcon"; else bad "colcon 없음"; fi

# 8. ~/.bashrc 설정
if grep -q "ros2-course" ~/.bashrc; then
  ok "~/.bashrc 설정 (ROS_DOMAIN_ID=$(grep -oP 'ROS_DOMAIN_ID=\K[0-9]+' ~/.bashrc | tail -1))"
else
  bad "~/.bashrc 설정 없음 - install_ros2_jazzy.sh 실행"
fi

# 9. GUI (WSLg)
if [[ -n "${DISPLAY:-}" || -n "${WAYLAND_DISPLAY:-}" ]]; then ok "GUI 표시 가능 (DISPLAY=${DISPLAY:-없음})"; else bad "DISPLAY 없음 - PowerShell에서 wsl --update"; fi

# 10. 렌더러 (GPU 없으면 llvmpipe가 정상)
if command -v glxinfo >/dev/null 2>&1; then
  RENDERER=$(glxinfo -B 2>/dev/null | grep -i "OpenGL renderer" | cut -d: -f2 | xargs)
  if [[ -z "$RENDERER" ]]; then bad "OpenGL 확인 실패"
  elif echo "$RENDERER" | grep -qi llvmpipe; then ok "렌더러 ${RENDERER} (CPU 렌더링)"
  else ok "렌더러 ${RENDERER}"; fi
else
  warn "glxinfo 없음 (sudo apt install mesa-utils)"
fi

echo
if (( FAIL == 0 )); then echo "결과: 실습 준비 완료"; else echo "결과: [실패] ${FAIL}건 - setup/README.md 문제 해결 표 참고"; fi
exit "$FAIL"
