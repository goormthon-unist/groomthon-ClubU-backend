import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename


def create_banner_directories(club_id):
    """배너 저장을 위한 디렉토리 생성"""
    base_dir = "banners"
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
                "file_path": (f"/banners/{club_id}/optimized/{optimized_filename}"),
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
    base_dir = "clubs"
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
                "file_path": f"/clubs/{club_id}/images/{optimized_filename}",
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
