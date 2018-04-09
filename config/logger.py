import logging
from logging.handlers import RotatingFileHandler

FALLBACK_FORMAT = '%(asctime)s [%(levelname)s] %(process)d#%(thread)d: %(name)s - %(message)s'


def init_logger(app, logger):
    level = getattr(logging, app.config['LOG_LEVEL'].upper())
    file_name = app.config['LOG_FILE_NAME']
    max_bytes = app.config['LOG_FILE_MAX_SIZE']
    backup_count = app.config['LOG_FILE_BACKUP_COUNT']
    
    logger.setLevel = level
    
    try:
        handler = RotatingFileHandler(file_name, maxBytes=max_bytes, backupCount=backup_count)
    except:
        handler = logging.StreamHandler()
    
    handler.setFormatter(fmt=FALLBACK_FORMAT)
    handler.setLevel(level)
    logger.addHandler(handler)
