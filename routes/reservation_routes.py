from flask_restx import Namespace
from controllers.reservation_controller import reservation_ns

# 네임스페이스 등록
__all__ = ["reservation_ns"]
