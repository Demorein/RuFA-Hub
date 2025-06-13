from core import Logger

def mainloop(data):
    a = Logger(__name__, "logs/test.log")
    a.info(data["data"])
