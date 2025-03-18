import psutil

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    ram_usage = ram_info.percent

    return {
        "CPU": f"{cpu_usage}",
        "RAM": f"{ram_usage}"
    }
