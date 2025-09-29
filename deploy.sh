#!/bin/bash

# ClubU Backend 배포 스크립트
# EC2 인스턴스에서 실행되는 스크립트

set -e  # 에러 발생 시 스크립트 중단

echo "=== ClubU Backend 배포 시작 ==="

# 변수 설정
APP_DIR="/home/ubuntu/groomthon-ClubU-backend"
CONTAINER_NAME="clubu-backend-container"
IMAGE_NAME="clubu-backend"
ENV_FILE="/home/ubuntu/.env"

# 애플리케이션 디렉토리로 이동 또는 클론
if [ -d "$APP_DIR" ]; then
    echo "애플리케이션 디렉토리로 이동: $APP_DIR"
    cd "$APP_DIR"
    
    echo "최신 코드 가져오기..."
    git fetch origin
    git reset --hard origin/main
    
    # 기존 이미지 폴더 제거 (리포 밖으로 분리)
    rm -rf banners clubs notices
else
    echo "애플리케이션 디렉토리가 없습니다. 리포지토리 클론..."
    cd /home/ubuntu
    git clone https://github.com/your-username/groomthon-ClubU-backend.git
    cd "$APP_DIR"
fi

# 환경 파일 확인
if [ ! -f "$ENV_FILE" ]; then
    echo "환경 파일이 없습니다: $ENV_FILE"
    echo "env.example을 참고하여 /home/ubuntu/.env 파일을 생성해주세요."
    exit 1
fi

echo "Docker 이미지 빌드..."
sudo docker build -t "$IMAGE_NAME" .

echo "기존 컨테이너 중지 및 제거..."
sudo docker stop "$CONTAINER_NAME" 2>/dev/null || echo "실행 중인 컨테이너가 없습니다."
sudo docker rm "$CONTAINER_NAME" 2>/dev/null || echo "제거할 컨테이너가 없습니다."

echo "새 컨테이너 실행..."
sudo docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p 5000:5000 \
    --env-file "$ENV_FILE" \
    --mount type=bind,source="$APP_DIR/banners",target=/data/banners \
    --mount type=bind,source="$APP_DIR/clubs",target=/data/clubs \
    --mount type=bind,source="$APP_DIR/notices",target=/data/notices \
    --entrypoint /bin/bash \
    "$IMAGE_NAME" -lc 'set -e;
    rm -rf /app/{banners,clubs,notices,cache} 2>/dev/null || true;
    ln -s /data/banners /app/banners;
    ln -s /data/clubs   /app/clubs;
    ln -s /data/notices /app/notices;
    exec python app.py'

echo "컨테이너 상태 확인..."
sleep 5
if sudo docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✅ 컨테이너가 성공적으로 실행되었습니다!"
    sudo docker logs "$CONTAINER_NAME" --tail 10
else
    echo "❌ 컨테이너 실행에 실패했습니다."
    sudo docker logs "$CONTAINER_NAME"
    exit 1
fi

echo "사용하지 않는 Docker 이미지 정리..."
sudo docker image prune -f

echo "=== 배포 완료! ==="
echo "API 엔드포인트: http://3.39.193.78:5000"
echo "도메인 엔드포인트: https://api.clubu.co.kr"
