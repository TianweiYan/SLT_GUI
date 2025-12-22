from loguru import logger
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, level='INFO')
