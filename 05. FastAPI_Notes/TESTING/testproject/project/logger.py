import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, info_log_file: str, error_log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    os.makedirs(os.path.dirname(info_log_file), exist_ok=True)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    for log_file in (info_log_file, error_log_file):
        handler = RotatingFileHandler(log_file, maxBytes=1 * 1024 * 1024, backupCount=5)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

log_files = {
    "celery": ("logs/celery_info.log", "logs/celery_error.log"),
    "main": ("logs/main_info.log", "logs/main_error.log"),
    "utils": ("logs/utils_info.log", "logs/utils_error.log"),
    "redis": ("logs/redis_info.log", "logs/redis_error.log"),
    "chart": ("logs/chart_info.log", "logs/chart_error.log"),
    "process": ("logs/process_info.log", "logs/process_error.log")
}

loggers = {name: setup_logger(name, *files) for name, files in log_files.items()}
