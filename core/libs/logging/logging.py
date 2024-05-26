import logging
import traceback

DEFAULT_LOGGER_NAME = "my_app"


class LogInfo(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

    @staticmethod
    def configure_logger(logger_name):
        logger = logging.getLogger(logger_name)
        # queue_handler = logging.getHandlerByName("queue_handler")
        # if queue_handler is not None:
        #     queue_handler.listener.start()
        #     atexit.register(queue_handler.listener.stop)
        return logger

    @staticmethod
    def debug(msg, logger_name=DEFAULT_LOGGER_NAME, *args, **kwargs):
        logger = LogInfo.configure_logger(logger_name)
        logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, logger_name=DEFAULT_LOGGER_NAME, *args, **kwargs):
        logger = LogInfo.configure_logger(logger_name)
        logger.info(msg, *args, **kwargs)

    @staticmethod
    def error(msg, logger_name=DEFAULT_LOGGER_NAME, *args, **kwargs):
        logger = LogInfo.configure_logger(logger_name)
        logger.error(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, logger_name=DEFAULT_LOGGER_NAME, *args, **kwargs):
        logger = LogInfo.configure_logger(logger_name)
        stack_trace = traceback.format_exc()
        logger.exception(msg, *args, **kwargs)


"""
Usage example :

LogInfo.info("HELLO")
"""
