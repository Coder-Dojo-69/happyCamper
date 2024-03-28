import psutil
import subprocess

# Function to check if the bot process is running
def is_bot_running():
    for proc in psutil.process_iter():
        if "python" in proc.name() and "main.py" in " ".join(proc.cmdline()):
            return True
    return False

# If bot is not running, start it
if not is_bot_running():
    subprocess.Popen(["python", "/home/dojopython/happyCamper/main.py"])
