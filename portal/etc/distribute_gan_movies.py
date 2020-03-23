import glob
import os

from portal import get_portal_ip_list

ips = get_portal_ip_list()

files = glob.glob("/Users/vs/personal/sync/projects/brahman/portal/media-no/bbgan/*.mp4")

files.sort()

counter = 0
flipper = False
for i, f in enumerate(files):
	#print(f)
	counter = i/2
	try:
		ip = ips[counter]

	except Exception as e:
		print(e)

	portal = "portal%02d" % (1+counter)
	flipper = not flipper
	if flipper:
		oname = "movie1.mp4"
	else:
		oname = "movie2.mp4"
	print(ip + " -> " + oname)
	cmd = "scp %s %s:~/%s" % (f, portal, oname)
	os.system(cmd)
	print(cmd)
	#print(counter)
