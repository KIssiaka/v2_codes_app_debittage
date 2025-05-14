def get_system_info():
    import platform
    import os

    system_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.architecture(),
        "hostname": platform.node(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
    }
    
    return system_info

def get_cpu_usage():
    import psutil

    return psutil.cpu_percent(interval=1)