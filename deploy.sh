#!/bin/bash
set -euo pipefail

# --- 동시 배포 방지 ---
exec 9>/tmp/clubu-deploy.lock
flock -n 9 || { echo "다른 배포 진행 중. 종료"; exit 1; }

echo "=== ClubU Backend 배포 시작 ==="

APP_DIR="/home/ubuntu/groomthon-ClubU-backend"
CONTAINER_NAME="clubu-backend-container"
IMAGE_NAME="clubu-backend"
ENV_FILE="/home/ubuntu/.env"

echo "기존 컨테이너 중지/제거..."
# 컨테이너 강제 종료
sudo docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

# 컨테이너 완전 제거 대기 (최대 ~10초)
echo "컨테이너 완전 제거 대기..."
for i in {1..10}; do
  if ! sudo docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    break
  fi
  sleep 1
done

# (선택) 점유 디버그: lsof/fuser로 디렉터리 점유 여부 체크
echo "[DEBUG] 디렉터리 점유 프로세스 확인:"
command -v lsof >/dev/null && lsof +D "$APP_DIR/banners" || true
command -v lsof >/dev/null && lsof +D "$APP_DIR/clubs"   || true
command -v lsof >/dev/null && lsof +D "$APP_DIR/notices" || true
command -v lsof >/dev/null && lsof +D "$APP_DIR/reservations" || true

if [ -d "$APP_DIR" ]; then
  echo "애플리케이션 디렉토리로 이동: $APP_DIR"
  cd "$APP_DIR"
  echo "최신 코드 가져오기..."
  git fetch origin
  git reset --hard origin/main
  
  # 혹시 남아있는 "호스트 rm" 코드 탐지
  echo "[DEBUG] 호스트 rm 코드 검사:"
  grep -RnE 'rm -rf .*banners|rm -rf .*clubs|rm -rf .*notices|rm -rf .*reservations' . || true
  
  # 안전한 정리: 런타임 폴더는 제외하고 정리
  echo "불필요한 파일 정리..."
  git clean -fdx -e banners/ -e clubs/ -e notices/ -e reservations/ || true
else
  echo "리포지토리 클론..."
  cd /home/ubuntu
  git clone https://github.com/goormthon-unist/groomthon-ClubU-backend.git
  cd "$APP_DIR"
fi

echo "런타임 데이터 디렉터리 준비..."
mkdir -p "$APP_DIR/banners" "$APP_DIR/clubs" "$APP_DIR/notices" "$APP_DIR/reservations"
chmod 0777 "$APP_DIR"/{banners,clubs,notices,reservations}

if [ ! -f "$ENV_FILE" ]; then
  echo "환경 파일이 없습니다: $ENV_FILE"
  exit 1
fi

echo "Docker 이미지 빌드..."
sudo docker build -t "$IMAGE_NAME" .

echo "컨테이너 실행..."
sudo docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  -p 5000:5000 \
  --env-file "$ENV_FILE" \
  --mount type=bind,source="$APP_DIR/banners",target=/data/banners \
  --mount type=bind,source="$APP_DIR/clubs",target=/data/clubs \
  --mount type=bind,source="$APP_DIR/notices",target=/data/notices \
  --mount type=bind,source="$APP_DIR/reservations",target=/data/reservations \
  --entrypoint /bin/bash \
  "$IMAGE_NAME" -lc 'set -e;
    rm -rf /app/{banners,clubs,notices,cache,reservations} 2>/dev/null || true;
    ln -s /data/banners /app/banners;
    ln -s /data/clubs   /app/clubs;
    ln -s /data/notices /app/notices;
    ln -s /data/reservations /app/reservations;
    exec python app.py'

echo "컨테이너 상태 확인..."
for i in {1..10}; do
  if sudo docker ps | grep -q "$CONTAINER_NAME"; then ok=1; break; fi
  sleep 1
done

if [ "${ok:-0}" -eq 1 ]; then
  echo "✅ 컨테이너 실행 OK"
  sudo docker logs "$CONTAINER_NAME" --tail 80 || true
else
  echo "❌ 컨테이너 실행 실패"
  sudo docker logs "$CONTAINER_NAME" || true
  exit 1
fi

echo "이미지 정리..."
sudo docker image prune -f

echo "=== 배포 완료! ==="
echo "API: http://13.124.12.61:5000"
echo "도메인: https://api.clubu.co.kr"
