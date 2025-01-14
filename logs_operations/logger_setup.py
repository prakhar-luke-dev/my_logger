import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_file="logs/chatlog", log_handler='my_logger', backup=15, rotate='midnight'):
    """
    Setup logger
    Args:
        log_file (str) : Path to log file
        log_handler (str) : handler name
        backup (int) : number of backup files to keep
        rotate (str[S,M,H,D,'midnight',W{0-6}]) : what time new file will be created \
                            (S - Seconds, M - Minutes, H - Hours, D - Days, midnight, \
                            W{0-6} - roll over on a certain day; 0 - Monday)

    Return:
        logger (object) : logger object with args property
    """
    logger = logging.getLogger(log_handler)
    # Check if logger already has handlers to avoid adding duplicate handlers
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        handler = TimedRotatingFileHandler(log_file, when=rotate, interval=1, backupCount=backup, utc=False)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
