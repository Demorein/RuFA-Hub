from os import path

def _time() -> str:
        import datetime
        dt = datetime.datetime.now()
        nowtime = dt.time()
        nowdate = dt.date()
        return(f"Time: {nowtime.hour}:{nowtime.minute}\nDate:{nowdate.day}.{nowdate.month}.{nowdate.year}")
    
    
def _datetime() -> str:
    import datetime
    dt = datetime.datetime.now()
    nowtime = dt.time()
    nowdate = dt.date()
    nowday, nowmounth, nowyear, nowhour, nowminute = nowdate.day, nowdate.month, nowdate.year, nowtime.hour, nowtime.minute
    
    mess = ""
    if len(str(nowday)) == 1:mess += f"0{nowday}"
    elif len(str(nowday)) == 2:mess += str(nowday)
        
    if len(str(nowmounth)) == 1:mess += f"-0{nowmounth}"
    elif len(str(nowmounth)) == 2:mess += f"-{nowmounth}"
        
    mess += f"-{nowyear}"
        
    if len(str(nowhour)) == 1:mess += f" 0{nowhour}"
    elif len(str(nowday)) == 2:mess += f" {nowhour}"
        
    if len(str(nowminute)) == 1:mess += f":0{nowminute}"
    elif len(str(nowday)) == 2:mess += f":{nowminute}"
    
    return(mess)


def _elogs(log:str, ecode:int, v = "INFO", file = "errlog", pathh = path.basename(__file__)) -> str: 
    logg = f"\n{_datetime()} | {(v).upper()} | {__name__}:<{pathh}>:{ecode} - {log}"
    with open(f"logs/{file}.log", "a", encoding='utf-8') as f:
        f.write(logg)