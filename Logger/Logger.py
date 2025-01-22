import logging
import sys
from pathlib import Path


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class DatabaseLogHandler(logging.Handler):
    """A logging handler that logs messages to a database."""

    def __init__(self, db):
        super().__init__()
        self.db = db

    def emit(self, record):
        """Log a record to the database."""
        try:
            # Extract the severity and message directly from the record
            severity = record.levelname
            message = record.getMessage()  # This gets the log message without any formatting

            # Truncate the message if it exceeds the column limit
            if len(message) > 8192:
                message = message[:8192]

            # Assuming the database's add_log_entry method can handle severity and message as separate arguments
            # Here, we don't need to format them together or include a timestamp, as the database will handle it
            self.db.add_log_entry(severity, message)
        except Exception as e:
            # Handle any errors during logging to database
            print(f"Failed to log to database: {e}")


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger(metaclass=Singleton):
    """ Logging class to log in a controlled fashion."""
    def __init__(self, log_file: str, database=None):
        # Create Data dir if it does not exist
        Path(Path(log_file).parent).mkdir(parents=True, exist_ok=True)

        LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
        logging.root.setLevel(logging.DEBUG)

        logging.basicConfig(filename=Path(log_file).as_posix(),
                            level=logging.DEBUG,
                            format=LOG_FORMAT,
                            filemode='a'
                            )

        console = logging.StreamHandler(stream=sys.stdout)
        console.setLevel(logging.INFO)
        console.setFormatter(CustomFormatter())
        self.logger = logging.getLogger('root')
        logging.getLogger().addHandler(console)

        if database is not None:
            db_handler = DatabaseLogHandler(database)
            db_handler.setLevel(logging.INFO)  # Adjust as needed
            db_handler.setFormatter(CustomFormatter())  # Use the custom formatter for the database logs
            self.logger.addHandler(db_handler)

    def get_logger(self):
        return self.logger
