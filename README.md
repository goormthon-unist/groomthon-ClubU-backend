# ClubU Backend

## 기술 스택

- **Backend Framework**: Flask
- **Database**: MySQL (AWS RDS)
- **ORM**: SQLAlchemy
- **Deployment**: AWS EC2
- **CI/CD**: GitHub Actions

## 프로젝트 구조

```
flask-backend/
├── controllers/     # 실제 API 로직
├── models/         # DB 모델 정의
├── routes/         # 각 기능별 blueprint 등록
├── services/       # OpenAI 통신 / 기타 유틸성 기능
├── static/         # 정적 파일 (이미지 등)
├── templates/      # HTML 렌더링 (필요 시)
├── app.py          # 애플리케이션 진입점
├── config.py       # 환경 변수 및 설정 파일
└── requirements.txt # Python 패키지 리스트
```

## 설치 및 실행

### 1. 가상환경 생성 및 패키지 설치

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. .env 파일 수동 생성

프로젝트 루트에 `.env` 파일을 직접 생성하고 다음 내용을 입력하세요:

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here-change-this-in-production

# MySQL RDS 설정
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
DB_PORT=3306
DB_NAME=clubu
DB_USER=your_username
DB_PASSWORD=your_password

# 데이터베이스 URL
DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### 3. 데이터베이스 연결 테스트

```bash
# Flask 앱 실행
python app.py
```

## 개발 도구

### 코드 품질 도구

- **Black**: 코드 포맷터
- **Flake8**: 코드 린터
- **isort**: import 정렬
- **Bandit**: 보안 린터
- **Safety**: 의존성 취약점 스캐너

### 설치

```bash
pip install -r requirements-dev.txt
```

### 사용법

```bash
# 코드 포맷팅
black .

# 린팅
flake8 .

# import 정렬
isort .

# 보안 검사
bandit -r .
safety check
```

## CI/CD

### GitHub Actions

- **CI/CD Pipeline**: 코드 품질 검사, 테스트, 빌드 검증
- **Deploy to AWS**: AWS EC2에 자동 배포

### 워크플로우 파일

- `.github/workflows/ci.yml`: CI/CD 파이프라인
- `.github/workflows/deploy.yml`: AWS 배포

## 데이터베이스 모델

### 주요 모델

- **User**: 사용자 정보
- **Club**: 동아리 정보
- **ClubCategory**: 동아리 분과
- **ClubMember**: 동아리 멤버
- **Application**: 동아리 지원서
- **ClubRecommendation**: 동아리 추천

### 관계

- User ↔ ClubMember (1:N)
- Club ↔ ClubMember (1:N)
- Club ↔ ClubCategory (N:1)
- Club ↔ Application (1:N)

## 보안

### 환경 변수

- `.env` 파일을 통해 민감한 정보 관리
- 데이터베이스 자격 증명, API 키 등은 절대 코드에 하드코딩하지 않음

### 데이터베이스

- AWS RDS를 통한 관리형 데이터베이스
- 보안 그룹을 통한 접근 제어

## API 문서

### 동아리 관련 API

- `GET /api/v1/clubs`: 동아리 전체 목록 조회
- `GET /api/v1/clubs/<id>`: 특정 동아리 상세 정보 조회

### 응답 형식

```json
{
  "status": "success",
  "count": 1,
  "clubs": [
    {
      "id": 1001,
      "name": "Astral",
      "activity_summary": "천체관측",
      "category": {
        "id": 1,
        "name": "학술 분과"
      },
      "recruitment_status": "CLOSED",
      "created_at": "2025-08-27T10:00:00",
      "updated_at": "2025-08-27T10:00:00"
    }
  ]
}
```

## 기여 가이드라인

### 코드 스타일

- Black 포맷터 사용
- Flake8 린터 규칙 준수
- 명확한 변수명과 함수명 사용

### 커밋 메시지

- 명확하고 설명적인 커밋 메시지 작성
- 영어로 작성 권장

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**테스트용 주석: CI/CD 워크플로우 테스트**
