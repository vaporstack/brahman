#!/usr/bin/env python
import os

with open("etc/portal-rpis.txt") as f:
	data = f.readlines()

addrs = [x.split().pop() for x in data]
#print(addrs)

res = ",".join(addrs)
print(res)

for a in addrs:
	#cmd = "ping %s" % a

	cmd = "rsync -avze ssh media/ %s:~/media/"
	# os.system(cmd)
