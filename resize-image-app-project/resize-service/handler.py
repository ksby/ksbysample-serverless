import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def resize(event, context):
    logger.info(event)
