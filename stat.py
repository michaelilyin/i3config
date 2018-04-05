from i3pystatus import Status, Module
from i3pystatus import IntervalModule
import getpass
import subprocess
import re

me = getpass.getuser() + " \uf17c"


class Mic(IntervalModule):
    interval = 1
    format = " {volume}"
    format_mute = " {volume}"
    color = "#FFFFFF"
    warn_color = "#FF9075"
    alert_color = "#FF0000"

    settings = (
        ("format", "format string used for output."),
        ("format_mute", "format string used for output."),
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
            "Front Left: Capture \d+ \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+Front Right: Capture \d+ \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+",
            stat)

        vol = round((int(res.group(1)) + int(res.group(3))) / 2)
        stat = res.group(2) == "on" or res.group(4) == "on"

        if stat:
            color = self.warn_color
        else:
            color = self.alert_color

        cdict = {
            "volume": vol,
        }

        if stat:
            frmt = self.format
        else:
            frmt = self.format_mute

        self.data = cdict
        self.output = {
            "full_text": frmt.format(**cdict),
            "color": color
        }


status = Status(
    logfile="/var/log/i3pystatus.log"
)

status.register("text", text=me)

status.register("clock", format="%a %-d %b %X")

status.register("xkblayout", format="{symbol}")

status.register("load", format="{avg1} {avg5} {avg15}")
status.register("cpu_usage_graph", format=" {usage:2.0f} {cpu_graph}", graph_style="braille-fill", hints={"separator": False})

status.register("mem", format=" {percent_used_mem:4.1f}")

status.register("temp", format=" {temp:2.0f}")

status.register("network", interface="enp4s0", format_up=" {v4cidr}")

status.register("pulseaudio", format=" {volume}", sink="0", format_muted=" {volume}")
status.register(Mic, format=" {volume}", format_mute=" {volume}", hints={"separator": False})

status.register("disk", path="/home", format="~{avail:6.2f}")
status.register("disk", path="/", format=" {avail:6.2f}", hints={"separator": False})

status.register("uptime", interval=60, format="{days}d {hours}:{mins}")

status.run()
