#!/usr/bin/env python3

import os
import subprocess
import time

start_time = time.time()
for i in range(1, 256):
	p = subprocess.Popen(['./dora.htm'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = p.communicate(bytes(str(i), 'utf-8'))
	out = out.decode()
	poll = p.poll()
	if poll != 0:
		#print(poll)
		continue
	else:
		print("This is i: ", i)
		print("This is out: ", out)
		print("This is poll: ", poll)
		print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
		#exit()
	del poll

#if "out of range" in out:
#	print(i)
	#continue
	#exit()
