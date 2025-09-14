import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename


def create_banner_directories(club_id):
    """배너 저장을 위한 디렉토리 생성"""
    base_dir = "banners"
    original_dir = os.path.join(base_dir, str(club_id), "original")
    optimized_dir = os.path.join(base_dir, str(club_id), "optimized")
    
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(optimized_dir, exist_ok=True)
    
    return original_dir, optimized_dir


def optimize_image(image_path, output_path, max_width=800, max_height=600, quality=85):
    """이미지 최적화 및 WebP 변환"""
    try:
        with Image.open(image_path) as img:
            # RGB로 변환 (WebP는 RGBA를 지원하지만 일관성을 위해 RGB 사용)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # 이미지 크기 조정 (비율 유지)
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # WebP로 저장
            img.save(output_path, 'WebP', quality=quality, optimize=True)
            
        return True
    except Exception as e:
        print(f"이미지 최적화 중 오류 발생: {str(e)}")
        return False


def save_banner_image(file, club_id):
    """배너 이미지 저장 및 최적화"""
    try:
        # 파일명 보안 처리
        filename = secure_filename(file.filename)
        if not filename:
            raise ValueError("유효하지 않은 파일명입니다")
        
        # 파일 확장자 확인
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if file_ext not in allowed_extensions:
            raise ValueError("지원하지 않는 파일 형식입니다")
        
        # 고유한 파일명 생성
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        optimized_filename = f"{uuid.uuid4()}.webp"
        
        # 디렉토리 생성
        original_dir, optimized_dir = create_banner_directories(club_id)
        
        # 원본 파일 저장 경로
        original_path = os.path.join(original_dir, unique_filename)
        
        # 파일 저장
        file.save(original_path)
        
        # 최적화된 파일 저장 경로
        optimized_path = os.path.join(optimized_dir, optimized_filename)
        
        # 이미지 최적화
        if optimize_image(original_path, optimized_path):
            # 최적화 완료 후 원본 파일 삭제
            if os.path.exists(original_path):
                os.remove(original_path)
                print(f"원본 이미지 삭제 완료: {original_path}")
            
            return {
                "original_url": f"/banners/{club_id}/original/{unique_filename}",
                "optimized_url": f"/banners/{club_id}/optimized/{optimized_filename}",
                "original_path": None,  # 원본은 삭제되었으므로 None
                "optimized_path": optimized_path
            }
        else:
            # 최적화 실패 시 원본 파일 삭제
            if os.path.exists(original_path):
                os.remove(original_path)
            raise ValueError("이미지 최적화에 실패했습니다")
            
    except Exception as e:
        raise Exception(f"이미지 저장 중 오류 발생: {str(e)}")


def delete_banner_images(original_path, optimized_path):
    """배너 이미지 파일 삭제"""
    try:
        # 원본 파일은 최적화 후 삭제되므로 존재할 수 없음
        # 하지만 안전을 위해 확인 후 삭제
        if original_path and os.path.exists(original_path):
            os.remove(original_path)
            print(f"원본 이미지 삭제: {original_path}")
        
        # 최적화된 파일 삭제
        if optimized_path and os.path.exists(optimized_path):
            os.remove(optimized_path)
            print(f"최적화된 이미지 삭제: {optimized_path}")
        
        return True
    except Exception as e:
        print(f"이미지 삭제 중 오류 발생: {str(e)}")
        return False
