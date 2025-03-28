import logging
from logging.handlers import TimedRotatingFileHandler
import logstash
from .formatter import JSONFormatter

def setup_logger(log_file="logs/app.log", log_handler="my_logger",
                 backup=15, rotate="midnight",
                 log_format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                 date_format="%Y-%m-%d %H:%M:%S",
                 _utc=False, use_json=False,
                 json_format=None, logstash_host=None, logstash_port=None):
    """
    Setup a logger with optional JSON formatting.
    
    Args:
        log_file (str): Path to log file.
        log_handler (str): Logger name.
        backup (int): Number of backups to keep.
        rotate (str): Rotation frequency (S, M, H, D, 'midnight', W{0-6}).
        log_format (str): Format for text logs.
        date_format (str): Format for timestamps.
        _utc (bool): Whether to use UTC timestamps.
        use_json (bool): Enable JSON format.
        json_format (dict): Custom JSON format mapping.
        logstash_host (str): Logstash server address.
        logstash_port (int): Logstash server port.

    Returns:
        logger (object): Configured logger.
    """
    logger = logging.getLogger(log_handler)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # File handler with rotation
        handler = TimedRotatingFileHandler(log_file, when=rotate, interval=1, backupCount=backup, utc=_utc)

        # Apply formatter
        if use_json:
            formatter = JSONFormatter(json_format=json_format, datefmt=date_format)
        else:
            formatter = logging.Formatter(log_format, datefmt=date_format)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Optional Logstash handler
        if logstash_host and logstash_port:
            logstash_handler = logstash.TCPLogstashHandler(logstash_host, logstash_port, version=1)
            logstash_handler.setFormatter(JSONFormatter(json_format=json_format, datefmt=date_format))
            logger.addHandler(logstash_handler)

    return logger
