from core import Logger
from time import sleep

def mainloop(data):
    a = Logger(__name__, "logs/test1.log")
    dataa = "asdasd"
    while True:
        sleep(1)
        a.info(dataa)