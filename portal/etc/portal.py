#!/usr/bin/env python
import os
import sys

def get_portal_ip_list():
	path = os.path.dirname(sys.argv[0])
	with open("%s/portal-rpis.txt" % path) as f:
		data = f.readlines()

	addrs = [x.split().pop() for x in data]
	#print(addrs)

	#res = ",".join(addrs)
	#print(res)

	#for a in addrs:
	#	#cmd = "ping %s" % a

	#	cmd = "rsync -avze ssh media/ %s:~/media/"
	#	# os.system(cmd)
	return addrs


if __name__ == "__main__":
	lst = get_portal_ip_list()
	print(lst)
