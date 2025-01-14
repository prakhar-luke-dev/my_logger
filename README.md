# my_logger

## how to use :
```python
from logs_operations.logger_setup import setup_logger

logger1 = setup_logger(log_file="logs/logfile_name", log_handler='logger1', backup=15)

logger2 = setup_logger(log_file="logs/logfile2_name", log_handler='logger2', backup=15)

logger1.info("this is written to logfile_name")
logger2.info("this is in logfile2_name")
```
