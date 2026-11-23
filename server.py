import json
import csv 
from datetime import datetime
import time
import shutil
import ctypes
import platform
from http.server import HTTPServer, BaseHTTPRequestHandler


# RAM information
def get_memory():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
        ]

    memory = MEMORYSTATUSEX()
    memory.dwLength = ctypes.sizeof(memory)

    ctypes.windll.kernel32.GlobalMemoryStatusEx(
        ctypes.byref(memory)
    )

    total = memory.ullTotalPhys
    used = total - memory.ullAvailPhys

    return {
        "total": round(total / (1024 ** 3), 2),
        "used": round(used / (1024 ** 3), 2),
        "percent": memory.dwMemoryLoad
    }


# CPU information
def get_cpu_times():
    class FILETIME(ctypes.Structure):
        _fields_ = [
            ("dwLowDateTime", ctypes.c_ulong),
            ("dwHighDateTime", ctypes.c_ulong)
        ]

    idle = FILETIME()
    kernel = FILETIME()
    user = FILETIME()

    ctypes.windll.kernel32.GetSystemTimes(
        ctypes.byref(idle),
        ctypes.byref(kernel),
        ctypes.byref(user)
    )

    def value(ft):
        return (ft.dwHighDateTime << 32) | ft.dwLowDateTime

    return value(idle), value(kernel), value(user)


previous_cpu = get_cpu_times()


def cpu_usage():
    global previous_cpu

    current = get_cpu_times()

    idle_delta = current[0] - previous_cpu[0]
    total_delta = (
        current[1] - previous_cpu[1]
        + current[2] - previous_cpu[2]
    )

    previous_cpu = current

    if total_delta == 0:
        return 0

    return round(
        100 * (total_delta - idle_delta) / total_delta, 1
    )


# Collect system metrics
def get_metrics():
    disk = shutil.disk_usage("C:\\")

    uptime = ctypes.windll.kernel32.GetTickCount64() / 1000

    return {
        "cpu": cpu_usage(),
        "memory": get_memory(),
        "disk": {
            "total": round(disk.total / (1024 ** 3), 2),
            "used": round(disk.used / (1024 ** 3), 2),
            "percent": round(disk.used / disk.total * 100, 1)
        },
        "uptime": int(uptime),
        "hostname": platform.node(),
        "os": platform.system() + " " + platform.release()
    }


# Save monitoring history
def save_log(data):

    file_name = "monitoring_log.csv"

    file_exists = False

    try:
        with open(file_name, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(file_name, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "CPU",
                "RAM",
                "Disk"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["cpu"],
            data["memory"]["percent"],
            data["disk"]["percent"]
        ])

# Web server
class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/metrics":

            metrics = get_metrics()
            save_log(metrics)
            data = json.dumps(metrics).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()

            self.wfile.write(data)

        elif self.path == "/" or self.path == "/dashboard.html":

            try:
                with open("dashboard.html", "rb") as file:
                    data = file.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()

                self.wfile.write(data)

            except FileNotFoundError:
                self.send_error(404, "dashboard.html not found")

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        print("Request:", args)


print("Server Monitoring Dashboard starting...")
print("Open http://localhost:8000 in your browser")

HTTPServer(("localhost", 8000), Handler).serve_forever()