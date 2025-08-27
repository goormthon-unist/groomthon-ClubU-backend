# ClubU Backend

Flask 기반의 동아리 관리 시스템 백엔드 API

## 🚀 기술 스택

- **Backend**: Flask 2.3.3
- **Database**: MySQL (AWS RDS)
- **ORM**: SQLAlchemy
- **Migration**: Flask-Migrate
- **CI/CD**: GitHub Actions
- **Code Quality**: Black, Flake8, isort, bandit

## 📁 프로젝트 구조

```
flask-backend/
│
├── controllers/      # API 로직
├── models/           # 데이터베이스 모델
├── routes/           # API 라우트
├── services/         # 비즈니스 로직
├── static/           # 정적 파일
├── templates/        # HTML 템플릿
├── .github/          # GitHub Actions
├── app.py            # 애플리케이션 진입점
├── config.py         # 설정 파일
└── requirements.txt  # 의존성 패키지
```

## 🛠️ 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 개발 도구
```

### 3. 환경변수 설정
`.env` 파일을 생성하고 다음 내용을 입력하세요:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key

# MySQL RDS 설정
DB_HOST=your-rds-endpoint
DB_PORT=3306
DB_NAME=clubu
DB_USER=your_username
DB_PASSWORD=your_password

DATABASE_URL=mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```

### 4. 애플리케이션 실행
```bash
python app.py
```

## 🔧 개발 도구

### 코드 품질 검사
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

### 테스트 실행
```bash
pytest
pytest --cov=. --cov-report=html
```

### Pre-commit hooks
```bash
pre-commit install
pre-commit run --all-files
```

## 🚀 CI/CD

### GitHub Actions
- **코드 품질 검사**: Black, Flake8, isort
- **보안 검사**: Bandit, Safety
- **테스트 실행**: Pytest
- **빌드 검증**: Flask 앱 생성 테스트

### 자동화된 워크플로우
1. `main` 또는 `develop` 브랜치에 푸시 시 자동 실행
2. Pull Request 시 코드 품질 검사
3. 모든 검사 통과 시 배포 가능

## 📊 데이터베이스 모델

- **User**: 사용자 정보
- **Club**: 동아리 정보
- **ClubMember**: 동아리 멤버십
- **ClubCategory**: 동아리 카테고리
- **Application**: 동아리 가입 신청
- **ApplicationAnswer**: 신청서 답변
- **ClubRecommendation**: 동아리 추천

## 🔐 보안

- 환경변수를 통한 민감 정보 관리
- `.env` 파일은 `.gitignore`에 포함
- 보안 취약점 자동 검사 (Bandit, Safety)

## 📝 API 문서

API 문서는 개발 진행에 따라 추가될 예정입니다.

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
