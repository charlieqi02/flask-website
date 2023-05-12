import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'CRITICAL': '\033[91m',    # red
        'ERROR': '\033[91m',       # red
        'WARNING': '\033[93m',     # yellow
        'INFO': '\033[92m',        # green
        'DEBUG': '\033[94m',        # blue   
    }

    def format(self, record):
        level = record.levelname
        color = self.COLORS[level]

        record.msg = f"{color}{record.msg}\033[0m"
        record.levelname = f"{color}[{record.levelname}]\033[0m"

        return super().format(record)


if __name__ == "__main__":
    logger = logging.getLogger("Test Logger")
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    logger.debug("This is a debug msg")
    logger.info("This is a info msg")
    logger.warning("This is a warning msg")
    logger.error("This is a error msg")
    logger.critical("This is a critical msg")