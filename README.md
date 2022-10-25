# Python Logger Module
A simple logging module that will write to a file and to the console.

The console output is in relevant colors.

The logger function is defined as a singleton so you can load it as many times
as you want it should not lock the log file even in multi-threaded applications.

## Usage

```python
from Logger import Logger

log_file = 'test.log'
logger = Logger(log_file).get_logger()

logger.info('Test')
logger.warn('Test')
logger.error('Test')
```