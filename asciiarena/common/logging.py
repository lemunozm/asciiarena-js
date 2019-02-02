import logging

logger = logging.getLogger("asciiarena")
logger.disabled = True

DEBUG_MESSAGE = 9
LEVEL_LIST = ["none", "debug-message", "debug", "info", "warning", "error", "critical"]

def message_log(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_MESSAGE):
        self._log(DEBUG_MESSAGE, message, args, **kws)

logging.Logger.debug_message = message_log

def init_logger(log_level):
    logging.addLevelName(DEBUG_MESSAGE, "MESSAGE")

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)


    level = {
        "none": logging.NOTSET,
        "debug-message": DEBUG_MESSAGE,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }[log_level]

    logger.addHandler(handler)
    logger.setLevel(level)
    logger.disabled = False
