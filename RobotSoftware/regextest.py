import re

msg = "<"

matches = re.findall(r'<(\d+):(\-?\d+\.\d+)>', "<1:0.001>", re.M|re.I)

print len(matches)
for match in matches:
    for i in match:
	print i