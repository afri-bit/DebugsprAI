import logging
import sys

# Define log format
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class CustomFormatter(logging.Formatter):
    """Custom formatter for colored logs in the console."""

    # ANSI escape sequences for colored output
    COLORS = {
        "DEBUG": "\033[92m",  # Green
        "INFO": "\033[94m",  # Blue
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[41m",  # Background Red
        "RESET": "\033[0m",
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        record.msg = f"{log_color}{record.msg}{self.COLORS['RESET']}"
        return super().format(record)


def setup_logger(name=None, level=logging.INFO):
    """Set up a logger that only logs to the console (no file logging)."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.hasHandlers():
        # Console Handler with color
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(CustomFormatter(LOG_FORMAT, datefmt=DATE_FORMAT))

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger
