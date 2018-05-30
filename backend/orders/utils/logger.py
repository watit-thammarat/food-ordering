import logging

from food_ordering.constants import APP_LOG


class Logger:
    logger = logging.getLogger(APP_LOG)

    @classmethod
    def log_info(cls, message):
        cls.logger.info(message)

    @classmethod
    def log_exception(cls, exception):
        if hasattr(exception, 'message'):
            cls.logger.error(exception.message)
        elif hasattr(exception, 'detail'):
            cls.logger.error(exception.detail)
        else:
            cls.logger.error(exception)
