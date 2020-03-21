import os


def get_cluster_ip_list():

	cluster = "10.79.20."
	cluster_low = 104
	cluster_high = 115

	res = []
	for x in range(cluster_low, 1 + cluster_high):
		ip = cluster + str(x)
		res.append(ip)

	return res
	#cmd = "ssh %s" % ip
	#os.system(cmd)
	# print(ip)


if __name__ == "__main__":
	ips = get_cluster_ip_list()
	print(ips)
