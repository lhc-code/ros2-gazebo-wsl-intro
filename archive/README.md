# archive

강의 준비·검증용. 학생 배포 자료는 [`practice/`](../practice/)에 있습니다.

| 경로 | 내용 |
|---|---|
| `check_code_sync.py` | `practice/*.md` 코드 블록과 `answers/` 파일 일치 검사 (CI에서도 실행) |

## 강의계획 변경 이력

| 시점 | 변경 |
|---|---|
| 초안 | 11/24(화) ~ 26(목) 3일, 2·3일차 각 6차시 (실습 12차시) |
| 변경 | 2일차(수) 오전 3차시만, 3일차(목) 6차시, 4일차(금) 현장실습 → 실습 9차시 |

변경으로 줄어든 3차시 처리:
- "Gazebo에 로봇 불러오기" + "키보드 주행" → 3일차 5차시로 합침
- "Gazebo 로봇 카메라 센서 추가" → 선택 과제로 이동 (`use_camera:=true`)
- "실습 결과 복습" → 3일차 6차시 뒤쪽 정리로 합침

## 실기 검증 체크리스트 (수업 전 실습실 PC 1대에서)

- [ ] `setup/install_ros2_jazzy.sh` 끝까지 실행, 소요 시간 기록
- [ ] `setup/check_env.sh` 전 항목 OK
- [ ] turtlesim · RViz 창 표시 (WSLg)
- [ ] `gazebo.launch.py` 기본(ogre2) / `render_engine:=ogre` 각각 창 표시 여부, 첫 화면까지 시간
- [ ] teleop 주행, `move_1m` 정지 위치 오차
- [ ] `use_camera:=true` 실행 시 RTF(real time factor) 저하 정도
- [ ] 검증 후 가이드의 `[미검증]` 표시 제거
