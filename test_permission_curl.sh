#!/bin/bash

# 권한 테스트용 curl 스크립트
BASE_URL="http://localhost:5000"

echo "🚀 권한 테스트 시작"
echo ""

# 1. 로그인
echo "1️⃣ abcde 사용자 로그인 (회장 권한)..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"tkfkd@unist.ac.kr","password":"wh1024"}' \
  -c cookies.txt)

echo "로그인 응답: $LOGIN_RESPONSE"
echo ""

# 2. 내 동아리 목록 조회
echo "2️⃣ 내가 속한 동아리 목록 조회..."
CLUBS_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/my-clubs" \
  -b cookies.txt)

echo "동아리 목록: $CLUBS_RESPONSE"
echo ""

# 3. HeXA 동아리에서 권한 확인
echo "3️⃣ HeXA 동아리에서 권한 확인..."
PERMISSION_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/clubs/53/my-permission" \
  -b cookies.txt)

echo "일반 권한 확인: $PERMISSION_RESPONSE"
echo ""

# 4. 회장 권한 확인
echo "4️⃣ 회장 권한 확인..."
PRESIDENT_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/clubs/53/my-permission?required_role=president" \
  -b cookies.txt)

echo "회장 권한 확인: $PRESIDENT_RESPONSE"
echo ""

# 5. 일반 사용자 권한 확인 (실패해야 함)
echo "5️⃣ 일반 사용자 권한 확인 (실패 예상)..."
NORMAL_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/clubs/53/my-permission?required_role=normal" \
  -b cookies.txt)

echo "일반 사용자 권한 확인: $NORMAL_RESPONSE"
echo ""

# 6. 로그아웃
echo "6️⃣ 로그아웃..."
LOGOUT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/logout" \
  -b cookies.txt)

echo "로그아웃 응답: $LOGOUT_RESPONSE"
echo ""

# 7. 로그아웃 후 권한 확인 (실패해야 함)
echo "7️⃣ 로그아웃 후 권한 확인 (실패 예상)..."
AFTER_LOGOUT_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/my-clubs" \
  -b cookies.txt)

echo "로그아웃 후 동아리 목록: $AFTER_LOGOUT_RESPONSE"
echo ""

# 8. xxx 사용자로 테스트 (일반 사용자)
echo "8️⃣ xxx 사용자 로그인 (일반 사용자)..."
XXX_LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"abcde@unist.ac.kr","password":"password123"}' \
  -c cookies_xxx.txt)

echo "xxx 로그인 응답: $XXX_LOGIN_RESPONSE"
echo ""

# 9. xxx 사용자의 HeXA 권한 확인
echo "9️⃣ xxx 사용자의 HeXA 권한 확인..."
XXX_PERMISSION_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/clubs/53/my-permission" \
  -b cookies_xxx.txt)

echo "xxx의 일반 권한: $XXX_PERMISSION_RESPONSE"
echo ""

# 10. xxx 사용자의 회장 권한 확인 (실패해야 함)
echo "🔟 xxx 사용자의 회장 권한 확인 (실패 예상)..."
XXX_PRESIDENT_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/roles/clubs/53/my-permission?required_role=president" \
  -b cookies_xxx.txt)

echo "xxx의 회장 권한: $XXX_PRESIDENT_RESPONSE"
echo ""

echo "🎉 권한 테스트 완료!"
echo "📋 예상 결과:"
echo "  - abcde: HeXA 회장 권한 (president)"
echo "  - xxx: HeXA 일반 사용자 권한 (normal)"
echo "  - 로그아웃 후: 권한 없음"
echo ""

# 쿠키 파일 정리
rm -f cookies.txt cookies_xxx.txt
