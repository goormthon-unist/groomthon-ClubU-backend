# Config package
import sys
import os

# 상위 디렉토리의 config.py를 직접 import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_module_path = os.path.join(parent_dir, "config.py")

# config.py를 동적으로 import
import importlib.util

spec = importlib.util.spec_from_file_location("config_module", config_module_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)

# config 객체를 현재 모듈로 가져오기
config = config_module.config

__all__ = ["config"]
