# 동아리 정보 수정 API 명세서

## 개요
동아리 회장이 동아리 정보를 수정할 수 있는 API들입니다. 모든 API는 회장 권한과 인증이 필요합니다.

## 공통 사항
- **인증**: 세션 기반 인증 필요
- **권한**: 동아리 회장 (CLUB_PRESIDENT) 권한 필요
- **Content-Type**: `application/json` (텍스트) 또는 `multipart/form-data` (파일)
- **Base URL**: `/api/v1/clubs/{club_id}`

## API 목록

### 1. 동아리 소개글 업로드/수정
- **Method**: `PUT`
- **Endpoint**: `/api/v1/clubs/{club_id}/introduction`
- **Description**: 동아리 소개글을 업로드하거나 수정합니다.
- **Headers**: 
  - `Content-Type: application/json`
  - `Cookie: session_id=...` (세션 인증)

**Request Body:**
```json
{
  "introduction": "동아리 소개글 내용입니다."
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "동아리 소개글이 성공적으로 업데이트되었습니다.",
  "club": {
    "id": 1003,
    "name": "HeXA",
    "introduction": "동아리 소개글 내용입니다.",
    "updated_at": "2025-01-20T10:30:00Z"
  }
}
```

### 2. 동아리 소개글 삭제
- **Method**: `DELETE`
- **Endpoint**: `/api/v1/clubs/{club_id}/introduction`
- **Description**: 동아리 소개글을 삭제합니다.
- **Headers**: 
  - `Cookie: session_id=...` (세션 인증)

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "동아리 소개글이 성공적으로 삭제되었습니다.",
  "club": {
    "id": 1003,
    "name": "HeXA",
    "introduction": null,
    "updated_at": "2025-01-20T10:30:00Z"
  }
}
```

### 3. 동아리 소개글 사진 업로드/수정
- **Method**: `PUT`
- **Endpoint**: `/api/v1/clubs/{club_id}/images/introduction`
- **Description**: 동아리 소개글 사진을 업로드하거나 수정합니다.
- **Headers**: 
  - `Content-Type: multipart/form-data`
  - `Cookie: session_id=...` (세션 인증)

**Request Body (Form Data):**
- `image`: 이미지 파일 (PNG, JPG, JPEG, GIF, BMP)

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "동아리 소개글 사진이 성공적으로 업데이트되었습니다.",
  "club": {
    "id": 1003,
    "name": "HeXA",
    "introduction_image": "/clubs/1003/images/introduction.webp",
    "updated_at": "2025-01-20T10:30:00Z"
  }
}
```

### 4. 동아리 소개글 사진 삭제
- **Method**: `DELETE`
- **Endpoint**: `/api/v1/clubs/{club_id}/images/introduction`
- **Description**: 동아리 소개글 사진을 삭제합니다.
- **Headers**: 
  - `Cookie: session_id=...` (세션 인증)

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "동아리 소개글 사진이 성공적으로 삭제되었습니다.",
  "club": {
    "id": 1003,
    "name": "HeXA",
    "introduction_image": null,
    "updated_at": "2025-01-20T10:30:00Z"
  }
}
```

### 5. 동아리 로고 사진 업로드/수정
- **Method**: `PUT`
- **Endpoint**: `/api/v1/clubs/{club_id}/images/logo`
- **Description**: 동아리 로고 사진을 업로드하거나 수정합니다.
- **Headers**: 
  - `Content-Type: multipart/form-data`
  - `Cookie: session_id=...` (세션 인증)

**Request Body (Form Data):**
- `image`: 이미지 파일 (PNG, JPG, JPEG, GIF, BMP)

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "동아리 로고 사진이 성공적으로 업데이트되었습니다.",
  "club": {
    "id": 1003,
    "name": "HeXA",
    "logo_image": "/clubs/1003/images/logo.webp",
    "updated_at": "2025-01-20T10:30:00Z"
  }
}
```

### 6. 동아리 로고 사진 삭제
- **Method**: `DELETE`
- **Endpoint**: `/api/v1/clubs/{club_id}/images/logo`
- **Description**: 동아리 로고 사진을 삭제합니다.
- **Headers**: 
  - `Cookie: session_id=...` (세션 인증)

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "동아리 로고 사진이 성공적으로 삭제되었습니다.",
  "club": {
    "id": 1003,
    "name": "HeXA",
    "logo_image": null,
    "updated_at": "2025-01-20T10:30:00Z"
  }
}
```

## 에러 응답

### 401 Unauthorized
```json
{
  "status": "error",
  "code": "401-01",
  "message": "로그인이 필요합니다."
}
```

### 403 Forbidden
```json
{
  "status": "error",
  "code": "403-01",
  "message": "동아리 회장 권한이 필요합니다."
}
```

### 404 Not Found
```json
{
  "status": "error",
  "code": "404-01",
  "message": "해당 동아리를 찾을 수 없습니다."
}
```

### 400 Bad Request
```json
{
  "status": "error",
  "code": "400-01",
  "message": "요청 데이터가 올바르지 않습니다."
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "code": "500-00",
  "message": "서버 내부 오류가 발생했습니다."
}
```

## 파일 저장 구조
```
clubs/
├── {club_id}/
│   ├── images/
│   │   ├── logo.webp
│   │   └── introduction.webp
│   └── original/ (원본 파일 저장 - 필요시)
│       ├── logo.{원본확장자}
│       └── introduction.{원본확장자}
```

## 이미지 처리 규칙
- 지원 형식: PNG, JPG, JPEG, GIF, BMP
- 최적화: WebP 형식으로 변환
- 압축: 품질 85%로 압축
- 크기 제한: 최대 800x600 픽셀 (비율 유지)
- 파일명: UUID 기반 고유 파일명 생성

## 권한 확인 로직
1. 세션 인증 확인
2. 사용자가 해당 동아리의 회장인지 확인
3. 동아리 존재 여부 확인
