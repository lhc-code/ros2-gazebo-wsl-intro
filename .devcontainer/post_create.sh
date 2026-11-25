#!/usr/bin/env bash
# Codespaces 첫 생성 시 1회 실행: ROS2 Jazzy + Gazebo Harmonic 설치, workspace 연결
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

bash "${REPO_DIR}/setup/install_ros2_jazzy.sh" 1

# WSL 가이드와 같은 경로(~/ros2_ws/src/ros2-gazebo-wsl-intro)로 쓸 수 있게 연결
mkdir -p ~/ros2_ws/src
ln -sfn "${REPO_DIR}" ~/ros2_ws/src/ros2-gazebo-wsl-intro

echo "준비 완료. 터미널을 새로 열고 'ros2 run turtlesim turtlesim_node'로 확인하세요."
