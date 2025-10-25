# Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libwebp-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pillow를 WebP 지원과 함께 재설치
RUN pip uninstall -y Pillow && pip install --no-cache-dir Pillow

# 애플리케이션 코드 복사 (필요한 파일들만)
COPY app.py .
COPY config.py .
COPY config/ ./config/
COPY controllers/ ./controllers/
COPY models/ ./models/
COPY routes/ ./routes/
COPY services/ ./services/
COPY utils/ ./utils/
COPY migrations/ ./migrations/
# static/과 templates/ 폴더는 선택적 (존재하지 않을 수 있음)

# 포트 5000 노출
EXPOSE 5000

# 환경변수 설정
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 심링크 생성 및 애플리케이션 실행
CMD ["bash", "-lc", "rm -rf /app/{banners,clubs,notices,cache,reservations} 2>/dev/null || true; ln -s /data/banners /app/banners; ln -s /data/clubs /app/clubs; ln -s /data/notices /app/notices; ln -s /data/cache /app/cache; ln -s /data/reservations /app/reservations; exec python app.py"]
