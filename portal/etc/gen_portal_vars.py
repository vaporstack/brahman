#!/usr/bin/env python

import os
import sys

from portal import get_portal_ip_list

# testing deployment
#from cluster import get_cluster_ip_list
#	portal tv map (not fact-checked):

ips = get_portal_ip_list()
#cluster_ips = get_cluster_ip_list()

#left='RRDDCCHHFFBBGGEEAA'
#right='KKLLQQJJNNPPIIMMOO'

left = "AABBCCDDEEFF"
right = "GGHHIIJJKKLL"
left_r = left[::2].lower()
right_r = right[::2].lower()
grid_map = left_r + right_r
print(grid_map)
# ipmap = [18,4,3,8,6,2,7,5,1,11,12,17,10,14,16,9,13,15]
ipmap = [1,6,7,2,4,8,3,5,9,0,0,0,0,0,0,0,0,0]
vmap  = list("abcdefghijkl")
def fmt( k, v):
	return "export %s=%s\n" % ( k.upper(), v)

count_x = 3
count_y = 3

size_x = 1280
size_y = 720

border_x = 250
border_y = 150

#total_x_pix = size_x * count_x
#total_y_pix = size_y * count_y

total_x = ((size_x + border_x) * count_x * 2) - border_x
total_y = ((size_y + border_y) * count_y) - border_x

num = 0
map_ctr = 0
v_ctr = 0
path = "gen"

if not os.path.exists(path):
	os.makedirs(path)



lut = {}
num = 0
for y in range(count_y):
	for x in range(count_x):
		translate_x = x * 2 * (size_x + border_x)
		translate_y = y * (size_y + border_y)
		idx = ipmap[num]
		num += 1
		#print(idx)
		lut[num] = (translate_x, translate_y)
print(lut)

# sys.exit()
num = 0

for y in range(count_y):
	for x in range(count_x):
	# print(x)

		portal_fmt = "portal%02d" % ipmap[num]

		hostname = "portal%02d" % (1 + num)
		fname = "%s/%s.txt" % (path, portal_fmt)
		with open(fname, 'w') as f:
			v = vmap[map_ctr]
			map_id = grid_map[map_ctr]
			print(map_id, v)
			f.write(fmt("portal","YES"))
			if v in left_r:
				f.write(fmt("side","NORTH"))
			else:
				f.write(fmt("side","SOUTH"))
			f.write(fmt("map_id", map_id))
			f.write(fmt("count_x", count_x))
			f.write(fmt("count_y", count_y))
			f.write(fmt("size_x", size_x))
			f.write(fmt("size_y", size_y))
			f.write(fmt("border_x", border_x))
			f.write(fmt("border_y", border_y))
			f.write(fmt("grid_id", num))
			f.write(fmt("total_x", total_x))
			f.write(fmt("total_y", total_y))
			print(total_x, total_y)
			# sys.exit()
			f.write(fmt("shift_x", 0))
			#idx = ipmap[num]
			translate_x, translate_y = lut[1+num]
			print(translate_x, translate_y)
			f.write(fmt("translate_x", translate_x))
			f.write(fmt("translate_y", translate_y))
			portal_fmt = "portal%02d" % ipmap[num]
			f.write(fmt("portal_id", portal_fmt))
			f.write(fmt("generated_order", num))
			print(portal_fmt, map_id)
		num+=1
		#if num/2 % 2 == 0:
		map_ctr += 1

		#v_ctr += 1

		cmd = "scp %s pi@%s:~/.portalrc" % (fname, portal_fmt)
		#print(cmd)
		os.system(cmd)
		#print(cmd)
