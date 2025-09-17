# 동아리 회장용 멤버 권한 관리 API 사용 가이드

## 📋 개요

동아리 회장이 자신의 동아리 내에서만 멤버들의 권한을 변경할 수 있는 API입니다.

## 🔐 권한 제한

- **CLUB_PRESIDENT**만 접근 가능
- **자신의 동아리 내에서만** 권한 변경 가능
- **동아리 내 역할만** 변경 가능 (CLUB_MEMBER, CLUB_OFFICER, CLUB_PRESIDENT)

## 🚀 API 엔드포인트

### 1. 동아리 멤버 목록 조회 (권한별 정렬)

**GET** `/api/v1/clubs/{club_id}/members/roles`

#### 요청 예시

```bash
curl -X GET http://localhost:5000/api/v1/clubs/1/members/roles
```

#### 응답 예시

```json
{
  "status": "success",
  "message": "동아리 '프로그래밍 동아리' 멤버 목록을 조회했습니다.",
  "data": {
    "club_id": 1,
    "club_name": "프로그래밍 동아리",
    "members": [
      {
        "user_id": 123,
        "user_name": "김회장",
        "user_email": "president@unist.ac.kr",
        "student_id": "20240001",
        "role_id": 4,
        "role_name": "CLUB_PRESIDENT",
        "role_description": "동아리 회장",
        "generation": 2,
        "other_info": "회장",
        "joined_at": "2025-09-15T10:00:00"
      },
      {
        "user_id": 124,
        "user_name": "박임원",
        "user_email": "officer@unist.ac.kr",
        "student_id": "20240002",
        "role_id": 3,
        "role_name": "CLUB_OFFICER",
        "role_description": "동아리 임원",
        "generation": 2,
        "other_info": "기획부장",
        "joined_at": "2025-09-16T11:00:00"
      },
      {
        "user_id": 125,
        "user_name": "이멤버",
        "user_email": "member@unist.ac.kr",
        "student_id": "20240003",
        "role_id": 2,
        "role_name": "CLUB_MEMBER",
        "role_description": "동아리 일반 멤버",
        "generation": 3,
        "other_info": "신입 멤버",
        "joined_at": "2025-09-17T12:00:00"
      }
    ],
    "total_count": 3
  }
}
```

### 2. 동아리 멤버 권한 변경 (개별)

**POST** `/api/v1/clubs/{club_id}/members/{user_id}/role`

#### 요청 예시

```bash
curl -X POST http://localhost:5000/api/v1/clubs/1/members/123/role \
  -H "Content-Type: application/json" \
  -d '{
    "role_name": "CLUB_OFFICER",
    "generation": 2,
    "other_info": "기획부장"
  }'
```

#### 요청 Body

```json
{
  "role_name": "CLUB_MEMBER" | "CLUB_OFFICER" | "CLUB_PRESIDENT",
  "generation": 1,  // 선택사항 (기본값: 1)
  "other_info": "기타 정보"  // 선택사항
}
```

#### 응답 예시

```json
{
  "status": "success",
  "message": "동아리 멤버 권한이 'CLUB_OFFICER'으로 변경되었습니다.",
  "data": {
    "user_id": 123,
    "user_name": "홍길동",
    "club_id": 1,
    "club_name": "프로그래밍 동아리",
    "role_name": "CLUB_OFFICER",
    "generation": 2,
    "other_info": "기획부장",
    "updated_at": "2025-09-17T09:00:00"
  }
}
```

### 3. 동아리 멤버 권한 조회

**GET** `/api/v1/clubs/{club_id}/members/{user_id}/role`

#### 요청 예시

```bash
curl -X GET http://localhost:5000/api/v1/clubs/1/members/123/role
```

#### 응답 예시

```json
{
  "status": "success",
  "message": "동아리 멤버 정보를 조회했습니다.",
  "data": {
    "user_id": 123,
    "user_name": "홍길동",
    "club_id": 1,
    "club_name": "프로그래밍 동아리",
    "role_name": "CLUB_OFFICER",
    "generation": 2,
    "other_info": "기획부장",
    "joined_at": "2025-09-15T10:00:00",
    "is_member": true
  }
}
```

### 4. 동아리 내 사용 가능한 역할 목록 조회

**GET** `/api/v1/clubs/roles`

#### 요청 예시

```bash
curl -X GET http://localhost:5000/api/v1/clubs/roles
```

#### 응답 예시

```json
{
  "status": "success",
  "message": "동아리 내 사용 가능한 역할 목록을 조회했습니다.",
  "data": {
    "roles": [
      {
        "role_id": 2,
        "role_name": "CLUB_MEMBER",
        "description": "동아리 일반 멤버"
      },
      {
        "role_id": 3,
        "role_name": "CLUB_OFFICER",
        "description": "동아리 임원"
      },
      {
        "role_id": 4,
        "role_name": "CLUB_PRESIDENT",
        "description": "동아리 회장"
      }
    ],
    "total_count": 3
  }
}
```

## 📝 사용 시나리오

### 시나리오 1: 동아리 멤버 목록 확인

```bash
# 동아리 멤버 목록 조회 (권한별 정렬)
curl -X GET http://localhost:5000/api/v1/clubs/1/members/roles
```

### 시나리오 2: 일반 멤버를 임원으로 승격 (개별)

```bash
# 1. 현재 역할 확인
curl -X GET http://localhost:5000/api/v1/clubs/1/members/123/role

# 2. CLUB_OFFICER로 승격
curl -X POST http://localhost:5000/api/v1/clubs/1/members/123/role \
  -H "Content-Type: application/json" \
  -d '{
    "role_name": "CLUB_OFFICER",
    "generation": 2,
    "other_info": "기획부장"
  }'
```

### 시나리오 3: 임원을 일반 멤버로 강등

```bash
# CLUB_MEMBER로 변경 (강등)
curl -X POST http://localhost:5000/api/v1/clubs/1/members/123/role \
  -H "Content-Type: application/json" \
  -d '{
    "role_name": "CLUB_MEMBER",
    "generation": 2
  }'
```

### 시나리오 4: 새 멤버 추가

```bash
# 동아리에 새 멤버 추가
curl -X POST http://localhost:5000/api/v1/clubs/1/members/456/role \
  -H "Content-Type: application/json" \
  -d '{
    "role_name": "CLUB_MEMBER",
    "generation": 3,
    "other_info": "신입 멤버"
  }'
```

## ⚠️ 주의사항

### 1. 권한 제한
- **CLUB_PRESIDENT**만 접근 가능
- **자신의 동아리 내에서만** 권한 변경 가능
- **동아리 내 역할만** 변경 가능 (전역 역할 변경 불가)

### 2. 허용된 역할
- `CLUB_MEMBER`: 동아리 일반 멤버
- `CLUB_OFFICER`: 동아리 임원
- `CLUB_PRESIDENT`: 동아리 회장

### 3. 제한된 역할
- `STUDENT`: 전역 역할 (변경 불가)
- `UNION_ADMIN`: 전역 관리자 (변경 불가)
- `DEVELOPER`: 개발자 (변경 불가)

## 🔒 보안 특징

### 1. 동아리 격리
- A동아리 회장은 A동아리 내에서만 권한 변경 가능
- B동아리 멤버의 권한은 변경 불가

### 2. 역할 제한
- 동아리 내 역할만 변경 가능
- 전역 역할은 변경 불가

### 3. 권한 검증
- 요청자가 해당 동아리의 회장인지 확인
- 대상 사용자가 해당 동아리의 멤버인지 확인

## 🚨 오류 처리

### 400 Bad Request
```json
{
  "message": "400-01: role_name is required"
}
```

### 403 Forbidden
```json
{
  "message": "권한 부족. 필요: CLUB_PRESIDENT, 현재: CLUB_MEMBER"
}
```

### 500 Internal Server Error
```json
{
  "message": "500-00: 서버 내부 오류가 발생했습니다 - 동아리 ID 999가 존재하지 않습니다."
}
```

## 🎯 활용 예시

### 프론트엔드에서의 사용

```javascript
// 1. 동아리 멤버 목록 조회
async function getClubMembers(clubId) {
  try {
    const response = await fetch(`/api/v1/clubs/${clubId}/members/roles`);
    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('멤버 목록:', result.data.members);
      return result.data.members;
    } else {
      console.error('멤버 목록 조회 실패:', result.message);
      return [];
    }
  } catch (error) {
    console.error('API 호출 오류:', error);
    return [];
  }
}

// 2. 개별 권한 변경
async function changeMemberRole(clubId, userId, roleName) {
  try {
    const response = await fetch(`/api/v1/clubs/${clubId}/members/${userId}/role`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        role_name: roleName,
        generation: 2,
        other_info: "기획부장"
      })
    });
    
    const result = await response.json();
    
    if (result.status === 'success') {
      console.log('권한 변경 성공:', result.data);
    } else {
      console.error('권한 변경 실패:', result.message);
    }
  } catch (error) {
    console.error('API 호출 오류:', error);
  }
}

// 사용 예시
async function manageClubMembers(clubId) {
  // 1. 멤버 목록 조회
  const members = await getClubMembers(clubId);
  
  // 2. 개별 권한 변경
  await changeMemberRole(clubId, 123, 'CLUB_OFFICER');
}

// 실행
manageClubMembers(1);
```

이제 동아리 회장이 자신의 동아리 내에서만 멤버들의 권한을 체계적으로 관리할 수 있습니다! 🎉
