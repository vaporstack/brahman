with open("portal-rpis.txt") as f:
	lines = f.readlines()

with open("out.txt", 'w') as off:
	off.write("\nHost portal*\n\tUser pi")
	off.write("\n\tIdentityFile ~/.ssh/id_rsa\n")

	for i,l in enumerate(lines):
		text = ("Host %s" % "portal%02d" % (1 + i))
		off.write("\n%s\n" % text)

		#off.write("\tUser pi")

		#print(l).split().pop()
		off.write("\tHostname %s" % l.split().pop())
		off.write("\n")
