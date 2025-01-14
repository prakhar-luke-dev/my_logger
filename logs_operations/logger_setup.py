import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(log_file="logs/chatlog", log_handler='my_logger', 
                 backup=15, rotate='midnight',
                 log_format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                 date_format="%Y-%m-%d %H:%M:%S",
                 _utc=False):
    """
    Setup logger with optional formatting.
    Args:
        log_file (str) : Path to log file
        log_handler (str) : handler name
        backup (int) : number of backup files to keep
        rotate (str[S,M,H,D,'midnight',W{0-6}]) : what time new file will be created \
                            (S - Seconds, M - Minutes, H - Hours, D - Days, midnight, \
                            W{0-6} - roll over on a certain day; 0 - Monday)
        log_format (str): Format for log messages.
        date_format (str): Format for the date in log messages.
        _utc (bool): Determines whether the timestamps for log rotation are based on UTC 

    Return:
        logger (object) : logger object with args property
    """
    logger = logging.getLogger(log_handler)
    # Check if logger already has handlers to avoid adding duplicate handlers
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        handler = TimedRotatingFileHandler(log_file, when=rotate, interval=1, backupCount=backup, utc=_utc)
        formatter = logging.Formatter(log_format, datefmt=date_format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)


    return logger
