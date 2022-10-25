import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


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
    def __init__(self, log_file: str):
        from pathlib import Path

        # Create Data dir if it does not exist
        Path(Path(log_file).parent).mkdir(parents=True, exist_ok=True)

        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.root.setLevel(logging.DEBUG)

        logging.basicConfig(filename=Path(log_file).as_posix(),
                            level=logging.DEBUG,
                            format=LOG_FORMAT,
                            filemode='a'
                            )

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(CustomFormatter())
        logging.getLogger().addHandler(console)

        self.logger = logging.getLogger('root')

    def get_logger(self):
        return self.logger
