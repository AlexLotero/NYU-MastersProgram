#!/usr/bin/env python3

import time

offsets = [52093, 7488, 40772, 17463, 19363, 43948, 339, 29455, 25794]
start_time = time.time()
for k in offsets:
    for UserInput1 in range(1, 256):
        for UserInput2 in range(1, 256):
            if (0x100 * UserInput1) + UserInput2 == k:# and UserInput1 <= 256 and UserInput2 <= 256:
                print("This is for offset ", k)
                print("This is UserInput1: ", UserInput1)
                print("This is UserInput2: ", UserInput2)
                print()
			    #exit()
            else:
                continue
    print("Execution Time: --- %s seconds ---" % (time.time() - start_time))
