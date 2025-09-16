# 관리자용 사용자 권한 변경 API 사용 가이드

## 개요
DEVELOPER 권한을 가진 관리자만 사용할 수 있는 사용자 권한 변경 API입니다.

## API 엔드포인트

### 1. 사용자 권한 변경 (권한 제거 포함)
**POST** `/api/v1/admin/users/{user_id}/roles`

#### 요청 본문
```json
{
    "club_id": 1,                    // 동아리 ID (선택사항, null이면 전역 권한)
    "role_name": "CLUB_PRESIDENT",   // 새로운 역할명 (필수)
    "generation": 5,                 // 기수 (선택사항)
    "other_info": "추가 정보"        // 기타 정보 (선택사항)
}
```

#### 사용 예시

**A동아리 멤버를 A동아리 회장으로 변경:**
```bash
curl -X POST http://localhost:5000/api/v1/admin/users/123/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": 1,
    "role_name": "CLUB_PRESIDENT",
    "generation": 5
  }'
```

**전역 관리자 권한 부여:**
```bash
curl -X POST http://localhost:5000/api/v1/admin/users/123/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": null,
    "role_name": "UNION_ADMIN"
  }'
```

**권한 제거 (STUDENT로 변경):**
```bash
curl -X POST http://localhost:5000/api/v1/admin/users/123/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": 1,
    "role_name": "STUDENT"
  }'
```

#### 응답 예시
```json
{
    "status": "success",
    "message": "사용자 김지원의 권한이 'CLUB_PRESIDENT'으로 변경되었습니다",
    "data": {
        "user_id": 123,
        "user_name": "김지원",
        "club_id": 1,
        "club_name": "UNIST 코딩클럽",
        "old_role": "CLUB_MEMBER",
        "new_role": "CLUB_PRESIDENT",
        "generation": 5,
        "changed_at": "2024-09-01T10:30:00"
    }
}
```

### 2. 사용자 권한 조회
**GET** `/api/v1/admin/users/{user_id}/roles`

#### 사용 예시
```bash
curl -X GET "http://localhost:5000/api/v1/admin/users/123/roles"
```

#### 응답 예시
```json
{
    "status": "success",
    "message": "사용자 권한 조회가 완료되었습니다",
    "data": {
        "user_id": 123,
        "user_name": "김지원",
        "user_email": "jiwon.kim@unist.ac.kr",
        "roles": [
            {
                "club_id": 1,
                "club_name": "UNIST 코딩클럽",
                "role_name": "CLUB_PRESIDENT",
                "generation": 5,
                "other_info": null,
                "joined_at": "2024-09-01T10:30:00"
            },
            {
                "club_id": null,
                "club_name": "전역",
                "role_name": "UNION_ADMIN",
                "generation": 1,
                "other_info": null,
                "joined_at": "2024-08-15T09:00:00"
            }
        ],
        "total_roles": 2
    }
}
```

### 3. 사용 가능한 역할 조회
**GET** `/api/v1/admin/roles`

#### 사용 예시
```bash
curl -X GET "http://localhost:5000/api/v1/admin/roles"
```

#### 응답 예시
```json
{
    "status": "success",
    "message": "사용 가능한 역할 목록 조회가 완료되었습니다",
    "data": {
        "roles": [
            {
                "id": 1,
                "role_name": "STUDENT",
                "description": "STUDENT 권한"
            },
            {
                "id": 2,
                "role_name": "CLUB_MEMBER",
                "description": "CLUB_MEMBER 권한"
            },
            {
                "id": 3,
                "role_name": "CLUB_OFFICER",
                "description": "CLUB_OFFICER 권한"
            },
            {
                "id": 4,
                "role_name": "CLUB_PRESIDENT",
                "description": "CLUB_PRESIDENT 권한"
            },
            {
                "id": 5,
                "role_name": "UNION_ADMIN",
                "description": "UNION_ADMIN 권한"
            },
            {
                "id": 6,
                "role_name": "DEVELOPER",
                "description": "DEVELOPER 권한"
            }
        ],
        "total_roles": 6
    }
}
```

## 권한 요구사항
- 모든 API는 **DEVELOPER** 권한이 필요합니다
- 로그인이 필요합니다
- 권한이 없는 경우 403 Forbidden 응답을 받습니다

## 에러 응답
```json
{
    "status": "error",
    "message": "400-01: role_name is required"
}
```

## 실제 사용 시나리오

### 시나리오 1: 동아리 회장 임명
```bash
# 1. 사용자 권한 조회
curl -X GET "http://localhost:5000/api/v1/admin/users/123/roles"

# 2. 일반 멤버를 회장으로 승격
curl -X POST http://localhost:5000/api/v1/admin/users/123/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": 1,
    "role_name": "CLUB_PRESIDENT",
    "generation": 5
  }'

# 3. 변경 결과 확인
curl -X GET "http://localhost:5000/api/v1/admin/users/123/roles"
```

### 시나리오 2: 전역 관리자 임명
```bash
# 전역 관리자 권한 부여
curl -X POST http://localhost:5000/api/v1/admin/users/456/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": null,
    "role_name": "UNION_ADMIN"
  }'
```

### 시나리오 3: 권한 다운그레이드
```bash
# 회장을 일반 멤버로 변경
curl -X POST http://localhost:5000/api/v1/admin/users/123/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": 1,
    "role_name": "CLUB_MEMBER"
  }'

# 전역 관리자를 일반 학생으로 변경
curl -X POST http://localhost:5000/api/v1/admin/users/123/roles \
  -H "Content-Type: application/json" \
  -d '{
    "club_id": null,
    "role_name": "STUDENT"
  }'
```

## 주의사항
1. **DEVELOPER 권한만 접근 가능**: 이 API는 시스템 관리자만 사용할 수 있습니다
2. **데이터 무결성**: 권한 변경 시 기존 멤버십을 업데이트하거나 새로 생성합니다
3. **캐시 무효화**: 권한 변경 후 사용자 권한 캐시가 자동으로 삭제됩니다
4. **트랜잭션**: 모든 변경사항은 트랜잭션으로 처리되어 오류 시 롤백됩니다
