# 동아리 컨텍스트 권한 시스템 가이드

## 개요
API 호출 시 해당 동아리에 속한 사용자인지 확인하는 컨텍스트 검사가 추가되었습니다.

## 🔧 개선된 권한 시스템

### 1. **동아리별 독립 권한**
- **A동아리 멤버**: A동아리에서만 `CLUB_MEMBER` 권한
- **B동아리 미가입**: B동아리에서는 권한 없음 (기본 `STUDENT`만)
- **전역 권한**: 모든 동아리에서 유효 (예: `UNION_ADMIN`, `DEVELOPER`)

### 2. **권한 검사 방식**

#### 기존 (전역 권한 검사)
```python
# 모든 권한을 합쳐서 검사 (보안 문제 가능)
user_roles = get_user_roles(user_id)  # 모든 권한 반환
```

#### 개선 (동아리 컨텍스트 검사)
```python
# 특정 동아리에서의 권한만 검사
user_roles = get_user_roles_in_club(user_id, club_id)  # 전역 + 해당 동아리 권한만
```

## 🎯 사용 방법

### 1. **데코레이터 사용**

#### 기본 사용법 (전역 권한 검사)
```python
@require_permission("clubs.update")
def patch(self, club_id):
    # 전역 권한 검사
    pass
```

#### 동아리 컨텍스트 사용법
```python
@require_permission("clubs.members", club_id_param="club_id")
def get(self, club_id):
    # club_id 파라미터를 동아리 컨텍스트로 사용
    pass
```

### 2. **서비스 직접 사용**

```python
from services.permission_service import permission_service

# 전역 권한 검사
result = permission_service.check_permission("clubs.update")

# 동아리 컨텍스트 권한 검사
result = permission_service.check_permission("clubs.members", club_id=1)
```

## 📋 실제 시나리오

### 시나리오 1: 동아리 멤버 목록 조회

**사용자 김지원의 권한:**
- 전역: `STUDENT`
- A동아리: `CLUB_MEMBER`
- B동아리: 권한 없음

**API 호출 결과:**

```bash
# A동아리 멤버 목록 조회 (성공)
GET /api/v1/clubs/1/members
# → A동아리에서 CLUB_MEMBER 권한으로 접근 가능

# B동아리 멤버 목록 조회 (실패)
GET /api/v1/clubs/2/members  
# → B동아리에서 권한 없음 (STUDENT만)
```

### 시나리오 2: 동아리 정보 수정

**사용자 박회장의 권한:**
- 전역: `STUDENT`
- A동아리: `CLUB_PRESIDENT`
- B동아리: 권한 없음

**API 호출 결과:**

```bash
# A동아리 정보 수정 (성공)
PATCH /api/v1/clubs/1
# → A동아리에서 CLUB_PRESIDENT 권한으로 접근 가능

# B동아리 정보 수정 (실패)
PATCH /api/v1/clubs/2
# → B동아리에서 권한 없음 (STUDENT만)
```

### 시나리오 3: 전역 관리자

**사용자 이관리자의 권한:**
- 전역: `UNION_ADMIN`
- A동아리: 권한 없음
- B동아리: 권한 없음

**API 호출 결과:**

```bash
# A동아리 멤버 목록 조회 (성공)
GET /api/v1/clubs/1/members
# → 전역 UNION_ADMIN 권한으로 접근 가능

# B동아리 멤버 목록 조회 (성공)
GET /api/v1/clubs/2/members
# → 전역 UNION_ADMIN 권한으로 접근 가능
```

## 🔒 보안 개선사항

### 1. **권한 격리**
- A동아리 권한으로 B동아리 API 접근 불가
- 각 동아리별 독립적인 권한 검사

### 2. **컨텍스트 인식**
- API 호출 시 해당 동아리 컨텍스트 자동 인식
- URL 파라미터에서 `club_id` 자동 추출

### 3. **전역 권한 우선**
- 전역 권한(`UNION_ADMIN`, `DEVELOPER`)은 모든 동아리에서 유효
- 동아리별 권한과 전역 권한을 모두 고려

## 🛠️ 구현된 기능

### 1. **권한 검사 서비스 개선**
- `check_permission(permission_key, user_id, club_id)` 메서드 추가
- `get_user_roles_in_club(user_id, club_id)` 메서드 추가

### 2. **데코레이터 개선**
- `@require_permission(permission_key, club_id_param="club_id")` 지원
- URL 파라미터에서 동아리 ID 자동 추출

### 3. **권한 조합 로직**
- 전역 권한 + 동아리별 권한 = 최종 권한
- 동아리별 권한이 없어도 전역 권한으로 접근 가능

## 📊 권한 매트릭스

| 사용자 | 전역 권한 | A동아리 | B동아리 | A동아리 API | B동아리 API |
|--------|-----------|---------|---------|-------------|-------------|
| 김학생 | STUDENT | - | - | ❌ | ❌ |
| 김멤버 | STUDENT | CLUB_MEMBER | - | ✅ | ❌ |
| 박회장 | STUDENT | CLUB_PRESIDENT | - | ✅ | ❌ |
| 이관리자 | UNION_ADMIN | - | - | ✅ | ✅ |
| 최개발자 | DEVELOPER | - | - | ✅ | ✅ |

## 🚀 사용 예시

### 컨트롤러에서 사용

```python
class ClubController(Resource):
    @require_permission("clubs.members", club_id_param="club_id")
    def get(self, club_id):
        # club_id=1인 경우, 사용자가 1번 동아리에서 권한이 있는지 확인
        # club_id=2인 경우, 사용자가 2번 동아리에서 권한이 있는지 확인
        pass
    
    @require_permission("clubs.update", club_id_param="club_id")
    def patch(self, club_id):
        # 해당 동아리에서 CLUB_PRESIDENT 이상 권한 필요
        pass
```

### 서비스에서 직접 사용

```python
def some_service_method(user_id, club_id):
    # 동아리 컨텍스트에서 권한 검사
    result = permission_service.check_permission(
        "clubs.members", 
        user_id=user_id, 
        club_id=club_id
    )
    
    if not result['has_permission']:
        raise PermissionError("권한이 없습니다")
    
    # 권한이 있는 경우에만 실행
    return get_club_members(club_id)
```

이제 **동아리별 권한 격리**가 완벽하게 구현되어 보안이 크게 향상되었습니다! 🎉
