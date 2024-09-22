#!/usr/bin/env python3

# (uVar2 & 0xf0f0f0f0) == 0xd0d0f0c0
# B = 0xf0f0f0f0 --> 4042322160 
# C = 0xd0d0f0c0 --> 3503354048

import time

def solve_for_A(B, C):
	i = 3489660928
	while 1:
		if (i & B) == C:
			A = i
			return A
		i = i + 1
start_time = time.time()
answer = solve_for_A(4042322160, 3503354048)
print("Execution Time: --- %s seconds ---" % (time.time() - start_time)) 
print("The script found the following answer: ", answer)
