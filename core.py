import logging
import os

class Logger:
    def __init__(self, name: str, logfile: str = None):
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

            # Консоль
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            # Файл (если указан)
            if logfile:
                os.makedirs(os.path.dirname(logfile), exist_ok=True)
                fh = logging.FileHandler(logfile, encoding="utf-8")
                fh.setFormatter(formatter)
                self.logger.addHandler(fh)

    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def critical(self, msg): self.logger.critical(msg)
    def exception(self, msg): self.logger.exception(msg)
