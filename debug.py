import subprocess
import locale
import re


# xset = subprocess.Popen(["xset", "-q"], stdout=subprocess.PIPE)
# grep = subprocess.Popen(["grep", "LED"], stdin=xset.stdout, stdout=subprocess.PIPE)
# lang = subprocess.check_output(["awk", "{ print $10 }"], stdin=grep.stdout).rstrip()
#
# out = lang
# if lang == "00000000":
#     out = "en"
# elif lang == "00001000":
#     out = "ru"
#
# print(out.decode("utf-8"))

# print(locale.getlocale(locale.LC_MESSAGES))

stat = subprocess.check_output(["/usr/bin/amixer", "get", "Capture"])
res = re.search("Front Left: Capture 46 \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+Front Right: Capture 46 \[(\d+)%\]\s\[\S+\]\s\[(on|off)\]\s+", stat)

vol = (int(res.group(1)) + int(res.group(3))) / 2

print(vol)