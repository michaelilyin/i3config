import subprocess
import locale
import re


stat = subprocess.check_output(["/usr/bin/amixer", "get", "Capture"])
res = re.search("Front Left: Capture 46 \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+Front Right: Capture 46 \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+", stat)

vol = (int(res.group(1)) + int(res.group(3))) / 2

print(vol)

