# ClubU Backend 배포 가이드

## 🚀 자동 배포 설정

### 1. GitHub Secrets 설정

GitHub 리포지토리의 Settings > Secrets and variables > Actions에서 다음 secrets를 추가하세요:

```
EC2_HOST=3.39.193.78
EC2_USERNAME=ubuntu
EC2_SSH_KEY=<EC2 인스턴스의 private key 내용>
```

### 2. EC2 인스턴스 초기 설정

EC2 인스턴스에 SSH로 접속하여 다음 명령어를 실행하세요:

```bash
# Docker 설치
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

# Git 설치
sudo apt install -y git

# 환경 변수 파일 생성
nano /home/ubuntu/.env
```

### 3. 환경 변수 설정 (.env 파일)

`/home/ubuntu/.env` 파일을 생성하고 다음 내용을 입력하세요:

```bash
# Flask 환경 설정
FLASK_ENV=production
SECRET_KEY=your-very-secret-key-here

# MySQL RDS 데이터베이스 설정
DATABASE_URL=mysql+pymysql://username:password@your-rds-endpoint:3306/database_name
```

### 4. 자동 배포 프로세스

1. `main` 브랜치에 코드를 push하면 자동으로 배포가 시작됩니다
2. GitHub Actions가 다음 단계를 실행합니다:
   - 코드 테스트 및 린팅
   - EC2 인스턴스에 SSH 접속
   - 최신 코드 가져오기
   - Docker 이미지 빌드
   - 컨테이너 재시작

## 🔧 수동 배포

수동으로 배포하려면 EC2 인스턴스에서 다음 스크립트를 실행하세요:

```bash
chmod +x deploy.sh
./deploy.sh
```

## 🏥 헬스체크

배포 후 다음 엔드포인트로 서비스 상태를 확인할 수 있습니다:

- **로컬**: http://3.39.193.78:5000/health
- **도메인**: https://api.clubu.co.kr/health

## 📋 API 엔드포인트

### 기본 엔드포인트
- `GET /` - API 정보
- `GET /health` - 헬스체크

### 동아리 관련
- `GET /api/v1/clubs` - 동아리 목록
- `GET /api/v1/clubs/{id}` - 동아리 상세 정보

## 🐛 트러블슈팅

### 1. 배포 실패 시

```bash
# 컨테이너 로그 확인
sudo docker logs clubu-backend-container

# 컨테이너 상태 확인
sudo docker ps -a

# 환경 변수 확인
sudo docker exec clubu-backend-container env
```

### 2. 데이터베이스 연결 오류

- RDS 보안 그룹에서 EC2 인스턴스의 IP 허용 확인
- 데이터베이스 엔드포인트 및 자격 증명 확인
- `.env` 파일의 `DATABASE_URL` 형식 확인

### 3. 포트 접근 문제

- EC2 보안 그룹에서 포트 5000 허용 확인
- 방화벽 설정 확인

## 🔐 보안 고려사항

1. **환경 변수**: 민감한 정보는 반드시 환경 변수로 관리
2. **SSH 키**: EC2 SSH 키를 안전하게 관리
3. **보안 그룹**: 필요한 포트만 허용
4. **SSL/TLS**: HTTPS 사용 (CloudFront 및 Certificate Manager 활용)

## 📊 모니터링

- CloudWatch를 통한 EC2 인스턴스 모니터링
- 애플리케이션 로그 확인: `sudo docker logs clubu-backend-container`
- 헬스체크 엔드포인트를 통한 서비스 상태 모니터링
