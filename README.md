# luke_logger

A flexible Python logging library that supports both standard and JSON-formatted logs.  
It can log to files and send logs to Logstash for centralized logging.

## how to use :
```bash
pip install luke-logger
```

#### Basic logger :

```python
from logs_operations.llogger import setup_logger

logger1 = setup_logger(log_file="logs/logfile_name", log_handler='logger1', backup=15)

logger2 = setup_logger(log_file="logs/logfile2_name", log_handler='logger2', backup=15)

logger1.info("this is written to logfile_name")
logger2.info("this is in logfile2_name")
```

#### Logger with JSON (for elk) :

```python
from logs_operations.llogger import setup_logger

json_format = {
    "time": "asctime",
    "log_level": "levelname",
    "msg": "message",
    "logger": "name",
    "file": "pathname",
    "line": "lineno",
    "func": "funcName",
}

logger = setup_logger(log_file="app.json", use_json=True, json_format=json_format)

logger.info("Logging in JSON format.")
```

#### Logstash Intergration
```python
from logs_operations.llogger import setup_logger

logger = setup_logger(logstash_host="127.0.0.1", logstash_port=5000, use_json=True)
logger.warning("This log will be sent to Logstash.")

```

# Future updates in line ->

#### Logger with bugsnag : 
```python
from logs_operations.llogger import setup_logger

bugsnag_logger = setup_logger(
    log_file="app/logs/app.log",
    log_handler="app-logger",
    bugsnag_config={
        "api_key": "your-bugsnag-api-key",
        "project_root": "app"
    },
    bugsnag_level=logging.WARNING  # Send warning and above to Bugsnag
)
```

#### Add bugsnag handler to other logger : 
```python
from logs_operations.llogger import add_bugsnag_to_logger
existing_logger = logger1 ## from above
enhanced_logger = add_bugsnag_to_logger(
    existing_logger,
    bugsnag_config={"api_key": "your-bugsnag-api-key"}
)
```


