from core import Logger, loop_extensions
from time import sleep

logger = Logger(__name__, "logs/test1.log")

@loop_extensions()
def mainloop(data):
    logger.info("test1")
    sleep(1)