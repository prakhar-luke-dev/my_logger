import logging
import json

class JSONFormatter(logging.Formatter):
    def __init__(self, json_format=None, datefmt=None):
        """
        Custom JSON formatter allowing flexible log formats.
        Args:
            json_format (dict): Maps log record attributes to JSON keys.
            datefmt (str): Date format string.
        """
        super().__init__(datefmt=datefmt)
        self.json_format = json_format or {
            "timestamp": "asctime",
            "level": "levelname",
            "message": "message",
            "logger": "name",
            "file": "pathname",
            "line": "lineno",
            "function": "funcName",
        }

    def format(self, record):
        """
        Formats log record as JSON using json_format mapping.
        """
        record_dict = record.__dict__
        log_entry = {json_key: record_dict.get(log_attr, None) for json_key, log_attr in self.json_format.items()}

        if "timestamp" in log_entry:
            log_entry["timestamp"] = self.formatTime(record)

        return json.dumps(log_entry)
