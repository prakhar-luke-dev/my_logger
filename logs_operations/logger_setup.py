import logging
import os
import json
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any


class LoggerSetup:
    def __init__(
        self,
        log_file="logs/chatlog",
        log_handler='my_logger',
        backup=15,
        rotate='midnight',
        log_format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        date_format="%Y-%m-%d %H:%M:%S",
        _utc=False,
        log_type='default',  # Options: 'default', 'json', 'bugsnag'
        custom_json_format: Optional[Dict[str, str]] = None,
        bugsnag_config: Optional[Dict[str, Any]] = None,
        bugsnag_level: int = logging.ERROR
    ):
        """
        Initialize logger with support for default, JSON (ELK), and Bugsnag logging formats.
        """
        self.log_file = log_file
        self.log_handler = log_handler
        self.backup = backup
        self.rotate = rotate
        self.log_format = log_format
        self.date_format = date_format
        self._utc = _utc
        self.log_type = log_type
        self.custom_json_format = custom_json_format
        self.bugsnag_config = bugsnag_config
        self.bugsnag_level = bugsnag_level
        self.logger = self._setup_logger()
    
    def _ensure_log_dir_exists(self):
        """Ensure the log directory exists."""
        log_path = Path(self.log_file)
        log_dir = log_path.parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger."""
        logger = logging.getLogger(self.log_handler)
        
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            self._ensure_log_dir_exists()
            
            file_handler = TimedRotatingFileHandler(
                self.log_file, when=self.rotate, interval=1, backupCount=self.backup, utc=self._utc
            )
            
            if self.log_type == 'json':
                formatter = self._get_json_formatter()
            else:
                formatter = logging.Formatter(self.log_format, datefmt=self.date_format)
            
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            if self.log_type == 'bugsnag' and self.bugsnag_config:
                self._setup_bugsnag(logger, formatter)
        
        return logger
    
    def _get_json_formatter(self):
        """Return a JSON formatter."""
        class JsonFormatter(logging.Formatter):
            def format(format_self, record):
                log_record = (
                    {key: getattr(record, value, "") for key, value in self.custom_json_format.items()}
                    if self.custom_json_format else
                    {
                        "timestamp": format_self.formatTime(record, self.date_format),
                        "name": record.name,
                        "level": record.levelname,
                        "filename": record.filename,
                        "lineno": record.lineno,
                        "message": record.getMessage()
                    }
                )
                return json.dumps(log_record)
        
        return JsonFormatter()
    
    def _setup_bugsnag(self, logger, formatter):
        """Set up Bugsnag integration."""
        try:
            import bugsnag
            from bugsnag.handlers import BugsnagHandler
            
            if not bugsnag.configuration.api_key:
                bugsnag.configure(**self.bugsnag_config)
            
            bugsnag_handler = BugsnagHandler()
            bugsnag_handler.setLevel(self.bugsnag_level)
            bugsnag_handler.setFormatter(formatter)
            logger.addHandler(bugsnag_handler)
            
            logger.info(f"Bugsnag integration enabled at level {logging.getLevelName(self.bugsnag_level)}")
        except ImportError:
            logger.warning("Bugsnag package not installed. Bugsnag integration disabled.")
        except Exception as e:
            logger.warning(f"Failed to configure Bugsnag: {str(e)}")
    
    def get_logger(self) -> logging.Logger:
        """Return the configured logger."""
        return self.logger