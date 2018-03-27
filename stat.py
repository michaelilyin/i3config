from i3pystatus import Status, Module
from i3pystatus import IntervalModule
import getpass
import subprocess
import re


class Lang(IntervalModule):
    interval = 1

    def run(self):
        xset = subprocess.Popen(["xset", "-q"], stdout=subprocess.PIPE)
        grep = subprocess.Popen(["grep", "LED"], stdin=xset.stdout, stdout=subprocess.PIPE)
        lang = subprocess.check_output(["awk", "{ print $10 }"], stdin=grep.stdout).rstrip()

        out = lang.decode("utf-8")
        if out == "00000000":
            out = "en"
        elif out == "00001000":
            out = "ru"

        self.output = {
            "full_text": out
        }


class Profile(IntervalModule):
    interval = 300

    def run(self):
        me = getpass.getuser()

        self.output = {
            "full_text": me
        }


class Mic(IntervalModule):
    """
    Shows memory load
    .. rubric:: Available formatters
    * {avail_mem}
    * {percent_used_mem}
    * {used_mem}
    * {total_mem}
    Requires psutil (from PyPI)
    """

    interval = 1
    format = "🎤 {volume}"
    color = "#FFFFFF"
    warn_color = "#FFFF00"
    alert_color = "#FF0000"
    warn_percentage = 100

    settings = (
        ("format", "format string used for output."),
        ("warn_percentage", "minimal percentage for warn state"),
        ("color", "standard color"),
        ("warn_color",
         "defines the color used when warn percentage is exceeded"),
        ("alert_color",
         "defines the color used when alert percentage is exceeded")
    )

    def run(self):
        stat = subprocess.check_output(["/usr/bin/amixer", "get", "Capture"]).decode("utf-8")
        res = re.search(
            "Front Left: Capture 46 \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+Front Right: Capture 46 \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+",
            stat)

        vol = round((int(res.group(1)) + int(res.group(3))) / 2)
        stat = res.group(2) == "on" or res.group(4) == "on"
        #
        # if psutil.version_info < (4, 4, 0):
        #     used = memory_usage.used - memory_usage.cached - memory_usage.buffers
        # else:
        #     used = memory_usage.used
        #
        if not stat:
            color = self.alert_color
        elif vol > self.warn_percentage:
            color = self.warn_color
        else:
            color = self.color

        cdict = {
            "volume": vol,
        }

        self.data = cdict
        self.output = {
            "full_text": self.format.format(**cdict),
            "color": color
        }


status = Status(
    logfile="/var/log/i3pystatus.log"
)

status.register(Profile)

status.register("clock", format="%a %-d %b %X")

status.register(Lang)

status.register("load", format="{avg1} {avg5} {avg15}")

status.register("cpu_usage_graph", format="{usage}% {cpu_graph}")
# status.register("cpu_usage_bar", bar_type="horizontal")

status.register("mem_bar", format="{used_mem_bar}", color="#4444FF")
status.register("swap", format="{percent_used}%")
status.register("mem", format="{percent_used_mem}%")

status.register("temp", format="🌡 {temp:.0f}°C")

status.register("network", interface="enp4s0", format_up="🌐 {v4cidr}")

status.register("pulseaudio", format="🎧 {volume}", sink="0")
status.register(Mic)

status.register("disk", path="/home", format="~ {avail}G")

status.register("disk", path="/", format="/ {avail}G")

status.run()
