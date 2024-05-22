import logging
from pathlib import Path


def create_specific_logger(logger_name, log_level=logging.DEBUG):
    file_path = (Path(__file__).parents[1] / 'logs').as_posix()
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    file = file_path + f"/{logger_name}.log"
    file_handler = logging.FileHandler(file)
    file_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger


error_logger = create_specific_logger('error', logging.ERROR)
