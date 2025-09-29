import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app


def create_banner_directories(club_id):
    """배너 저장을 위한 디렉토리 생성"""
    base_dir = current_app.config.get("BANNERS_DIR", "banners")
    optimized_dir = os.path.join(base_dir, str(club_id), "optimized")

    os.makedirs(optimized_dir, exist_ok=True)

    return optimized_dir


def optimize_image(image_path, output_path, max_width=800, max_height=600, quality=85):
    """이미지 최적화 및 WebP 변환"""
    try:
        with Image.open(image_path) as img:
            # RGB로 변환 (WebP는 RGBA를 지원하지만 일관성을 위해 RGB 사용)
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGB")

            # 이미지 크기 조정 (비율 유지)
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # WebP로 저장
            img.save(output_path, "WebP", quality=quality, optimize=True)

        return True
    except Exception as e:
        print(f"이미지 최적화 중 오류 발생: {e}")
        return False


def save_banner_image(file, club_id):
    """배너 이미지 저장 및 최적화"""
    try:
        from flask import current_app

        current_app.logger.info(
            f"Saving banner image: {file.filename} for club_id: {club_id}"
        )

        # 파일명 보안 처리
        filename = secure_filename(file.filename)
        if not filename:
            current_app.logger.error("Invalid filename")
            raise ValueError("유효하지 않은 파일명입니다")

        # 파일 확장자 확인
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "bmp"}
        file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
        if file_ext not in allowed_extensions:
            raise ValueError("지원하지 않는 파일 형식입니다")

        # 고유한 파일명 생성 (WebP로 저장)
        optimized_filename = f"{uuid.uuid4()}.webp"

        # 디렉토리 생성
        optimized_dir = create_banner_directories(club_id)
        current_app.logger.info(f"Created directory: {optimized_dir}")

        # 최적화된 파일 저장 경로
        optimized_path = os.path.join(optimized_dir, optimized_filename)

        # 임시 원본 파일 저장
        temp_path = os.path.join(optimized_dir, f"temp_{uuid.uuid4()}.{file_ext}")
        file.save(temp_path)
        current_app.logger.info(f"Saved temp file: {temp_path}")

        # 이미지 최적화
        if optimize_image(temp_path, optimized_path):
            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)

            current_app.logger.info(
                f"Banner image saved successfully: {optimized_path}"
            )
            return {
                "file_path": (
                    f"/{current_app.config.get('BANNERS_DIR', 'banners')}/{club_id}/optimized/{optimized_filename}"
                ),
                "optimized_path": optimized_path,
            }
        else:
            # 최적화 실패 시 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)
            current_app.logger.error("Image optimization failed")
            raise ValueError("이미지 최적화에 실패했습니다")

    except Exception as e:
        from flask import current_app

        current_app.logger.exception(f"Banner image save failed: {e}")
        raise Exception(f"이미지 저장 중 오류 발생: {e}")


def delete_banner_image(file_path):
    """배너 이미지 파일 삭제"""
    try:
        # 최적화된 파일 삭제
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"배너 이미지 삭제: {file_path}")

        return True
    except Exception as e:
        print(f"이미지 삭제 중 오류 발생: {e}")
        return False


def create_club_directories(club_id):
    """동아리 이미지 저장을 위한 디렉토리 생성"""
    base_dir = current_app.config.get("CLUBS_DIR", "clubs")
    club_dir = os.path.join(base_dir, str(club_id))
    images_dir = os.path.join(club_dir, "images")
    original_dir = os.path.join(club_dir, "original")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(original_dir, exist_ok=True)

    return images_dir, original_dir


def save_club_image(file, club_id, image_type):
    """동아리 이미지 저장 및 최적화 (로고 또는 소개글 이미지)"""
    try:
        # 파일명 보안 처리
        filename = secure_filename(file.filename)
        if not filename:
            raise ValueError("유효하지 않은 파일명입니다")

        # 파일 확장자 확인
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "bmp"}
        file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
        if file_ext not in allowed_extensions:
            raise ValueError("지원하지 않는 파일 형식입니다")

        # 이미지 타입 검증
        if image_type not in ["logo", "introduction"]:
            raise ValueError("유효하지 않은 이미지 타입입니다")

        # 고유한 파일명 생성 (WebP로 저장)
        optimized_filename = f"{image_type}_{uuid.uuid4()}.webp"

        # 디렉토리 생성
        images_dir, original_dir = create_club_directories(club_id)

        # 최적화된 파일 저장 경로
        optimized_path = os.path.join(images_dir, optimized_filename)

        # 임시 원본 파일 저장
        temp_path = os.path.join(original_dir, f"temp_{uuid.uuid4()}.{file_ext}")
        file.save(temp_path)

        # 이미지 최적화
        if optimize_image(temp_path, optimized_path):
            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)

            return {
                "file_path": f"/{current_app.config.get('CLUBS_DIR', 'clubs')}/{club_id}/images/{optimized_filename}",
                "optimized_path": optimized_path,
            }
        else:
            # 최적화 실패 시 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise ValueError("이미지 최적화에 실패했습니다")

    except Exception as e:
        raise Exception(f"이미지 저장 중 오류 발생: {e}")


def delete_club_image(file_path):
    """동아리 이미지 파일 삭제"""
    try:
        # 최적화된 파일 삭제
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"동아리 이미지 삭제: {file_path}")

        return True
    except Exception as e:
        print(f"이미지 삭제 중 오류 발생: {e}")
        return False


def create_notice_directories(notice_id):
    """공지사항 파일 저장을 위한 디렉토리 생성"""
    from flask import current_app

    base_dir = current_app.config.get("NOTICES_DIR", "notices")
    notice_dir = os.path.join(base_dir, str(notice_id))
    images_dir = os.path.join(notice_dir, "images")
    files_dir = os.path.join(notice_dir, "files")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(files_dir, exist_ok=True)

    return images_dir, files_dir


def save_notice_image(file, notice_id):
    """공지사항 이미지 저장 및 최적화"""
    try:
        from flask import current_app

        current_app.logger.info(
            f"Saving notice image: {file.filename} for notice_id: {notice_id}"
        )

        # 파일명 보안 처리
        original_filename = file.filename

        # 한글 파일명 처리를 위해 확장자를 먼저 추출
        if "." in original_filename:
            file_ext = original_filename.rsplit(".", 1)[1].lower()
        else:
            file_ext = ""

        # 파일 확장자 확인
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "bmp"}
        if file_ext not in allowed_extensions:
            raise ValueError(
                f"지원하지 않는 이미지 형식입니다. 허용된 형식: {', '.join(allowed_extensions)}. 업로드한 파일: {original_filename} (확장자: '{file_ext}')"
            )

        # 고유한 파일명 생성 (WebP로 저장)
        optimized_filename = f"{uuid.uuid4()}.webp"

        # 디렉토리 생성
        images_dir, files_dir = create_notice_directories(notice_id)
        current_app.logger.info(f"Created directory: {images_dir}")

        # 최적화된 파일 저장 경로
        optimized_path = os.path.join(images_dir, optimized_filename)

        # 임시 원본 파일 저장
        temp_path = os.path.join(images_dir, f"temp_{uuid.uuid4()}.{file_ext}")
        file.save(temp_path)
        current_app.logger.info(f"Saved temp file: {temp_path}")

        # 이미지 최적화
        if optimize_image(temp_path, optimized_path):
            # 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)

            current_app.logger.info(
                f"Notice image saved successfully: {optimized_path}"
            )
            return {
                "file_path": f"/{current_app.config.get('NOTICES_DIR', 'notices')}/{notice_id}/images/{optimized_filename}",
                "optimized_path": optimized_path,
            }
        else:
            # 최적화 실패 시 임시 파일 삭제
            if os.path.exists(temp_path):
                os.remove(temp_path)
            current_app.logger.error("Image optimization failed")
            raise ValueError("이미지 최적화에 실패했습니다")

    except Exception as e:
        from flask import current_app

        current_app.logger.exception(f"Notice image save failed: {e}")
        raise Exception(f"이미지 저장 중 오류 발생: {e}")


def save_notice_file(file, notice_id):
    """공지사항 문서 파일 저장 (엑셀, 워드, 한글, PPT 등)"""
    try:
        from flask import current_app

        current_app.logger.info(
            f"Saving notice file: {file.filename} for notice_id: {notice_id}"
        )

        # 파일명 보안 처리
        original_filename = file.filename

        # 한글 파일명 처리를 위해 확장자를 먼저 추출
        if "." in original_filename:
            file_ext = original_filename.rsplit(".", 1)[1].lower()
            # 확장자만으로 파일명 생성 (한글 문제 해결)
            filename = f"uploaded_file.{file_ext}"
        else:
            filename = "uploaded_file"

        current_app.logger.info(f"Original filename: {original_filename}")
        current_app.logger.info(f"Processed filename: {filename}")

        if not filename:
            current_app.logger.error("Invalid filename")
            raise ValueError("유효하지 않은 파일명입니다")

        # 파일 확장자 확인
        allowed_extensions = {
            # Microsoft Office
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            # 한글과컴퓨터
            "hwp",
            "hwpx",
            # 기타 문서
            "pdf",
            "txt",
            "rtf",
            "md",  # Markdown
            "csv",  # CSV 파일
            "json",  # JSON 파일
            # 압축 파일
            "zip",
            "rar",
            "7z",
            "tar",
            "gz",
            # 이미지 파일 (파일 업로드에서도 허용)
            "jpg",
            "jpeg",
            "png",
            "gif",
            "bmp",
            "webp",
            # 기타
            "exe",  # 실행 파일
            "apk",  # 안드로이드 앱
            "ipa",  # iOS 앱
        }
        # 이미 위에서 추출한 확장자 사용
        current_app.logger.info(f"File extension: '{file_ext}'")
        current_app.logger.info(f"Allowed extensions: {allowed_extensions}")

        if file_ext not in allowed_extensions:
            raise ValueError(
                f"지원하지 않는 파일 형식입니다. 허용된 형식: {', '.join(sorted(allowed_extensions))}. 업로드한 파일: {original_filename} (확장자: '{file_ext}')"
            )

        # 파일 크기 제한 (50MB)
        file.seek(0, 2)  # 파일 끝으로 이동
        file_size = file.tell()
        file.seek(0)  # 파일 시작으로 이동

        if file_size > 50 * 1024 * 1024:  # 50MB
            raise ValueError("파일 크기가 너무 큽니다 (최대 50MB)")

        # 고유한 파일명 생성 (원본 확장자 유지)
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        # 디렉토리 생성
        images_dir, files_dir = create_notice_directories(notice_id)
        current_app.logger.info(f"Created directory: {files_dir}")

        # 파일 저장 경로
        file_path = os.path.join(files_dir, unique_filename)

        # 파일 저장
        file.save(file_path)
        current_app.logger.info(f"Notice file saved successfully: {file_path}")

        return {
            "file_path": f"/{current_app.config.get('NOTICES_DIR', 'notices')}/{notice_id}/files/{unique_filename}",
            "original_filename": filename,
            "file_size": file_size,
        }

    except Exception as e:
        from flask import current_app

        current_app.logger.exception(f"Notice file save failed: {e}")
        raise Exception(f"파일 저장 중 오류 발생: {e}")


def delete_notice_asset(file_path):
    """공지사항 첨부파일 삭제"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"공지사항 첨부파일 삭제: {file_path}")

        return True
    except Exception as e:
        print(f"첨부파일 삭제 중 오류 발생: {e}")
        return False
