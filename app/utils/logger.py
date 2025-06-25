# app/utils/logger.py

import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(name)s: %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
