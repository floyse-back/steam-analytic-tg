import logging
import os
import sys


def startup_logger_configure():
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                        handlers=[
                            logging.StreamHandler(sys.stdout),
                        ]
                )

name_level = {
    "domain":"src/infrastructure/logger/logs/domain.log",
    "application":"src/infrastructure/logger/logs/application.log",
    "api":"src/infrastructure/logger/logs/api.log",
    "infrastructure":"src/infrastructure/logger/logs/infrastructure.log",
    "celery_app":"src/infrastructure/logger/logs/celery_app.log",
    "tests":"src/infrastructure/logger/logs/tests.log",
}

def get_logger(name: str, file_path: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_path = name_level.get(file_path)
    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_path) for h in logger.handlers):
            fh = logging.FileHandler(log_path, encoding='utf-8')
            fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            logger.addHandler(fh)

    return logger