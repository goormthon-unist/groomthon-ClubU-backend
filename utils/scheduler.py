"""
스케줄러 유틸리티
백그라운드 작업을 위한 스케줄러 설정
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import logging

logger = logging.getLogger(__name__)


def init_scheduler(app):
    """스케줄러 초기화 및 시작"""
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Seoul"))

    # Flask 앱 컨텍스트를 스케줄러 작업에 전달하기 위해 래퍼 함수 생성
    def job_wrapper():
        with app.app_context():
            archive_expired_banners_job()

    # 매일 자정(KST)에 만료된 배너 아카이브
    scheduler.add_job(
        func=job_wrapper,
        trigger=CronTrigger(hour=0, minute=0, timezone=pytz.timezone("Asia/Seoul")),
        id="archive_expired_banners",
        name="만료된 배너 자동 아카이브",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        "스케줄러가 시작되었습니다. 매일 자정(KST)에 만료된 배너를 아카이브합니다."
    )

    return scheduler


def archive_expired_banners_job():
    """만료된 배너를 ARCHIVED로 변경하는 스케줄러 작업"""
    try:
        from services.banner_service import archive_expired_banners

        archived_count = archive_expired_banners()
        if archived_count > 0:
            logger.info(f"만료된 배너 {archived_count}개를 ARCHIVED로 변경했습니다.")
        else:
            logger.debug("아카이브할 만료된 배너가 없습니다.")
    except Exception as e:
        logger.error(
            f"배너 아카이브 스케줄러 작업 중 오류 발생: {str(e)}", exc_info=True
        )
