import logging

logger = logging.getLogger("asciiarena")
logger.disabled = True

def init_logger(log_level):
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    level = {
        "none": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }[log_level]

    logger.addHandler(handler)
    logger.setLevel(level)
    logger.disabled = False
