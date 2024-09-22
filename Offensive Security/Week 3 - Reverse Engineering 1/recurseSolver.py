#!/usr/bin/env python3

import os
import subprocess
import time

start_time = time.time()
for i in range(1, 10000):
	for j in range(1, 10000):
		p = subprocess.Popen(['./recurse.bin'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = p.communicate(bytes(str(i) + " " + str(j), "utf-8"))
		out = out.decode()
		if "Nope" in out:
			continue
		else:
			print("This is i: ", i)
			print("This is j: ", j)
			print(out)
			print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
			exit()

