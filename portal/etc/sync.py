#!/usr/bin/env python
import os

from portal import get_portal_ip_list
from cluster import get_cluster_ip_list


if __name__ == "__main__":
	portals = get_portal_ip_list()
	clusters = get_cluster_ip_list()
	print("portals", portals)
	print("clusters", clusters)

	for i,ip in enumerate(portals):
		dst = "portal%02d" % (1+i)
		cmd = "rsync -avze ssh --exclude='*.app' --partial --exclude='.DS_Store' ~/personal/sync/projects/brahman/portal/media/ %s:~/media &" %  dst

		#cmd = "ssh %s" % dst
		#os.system(cmd)
		# print(cmd)
		os.system(cmd)
