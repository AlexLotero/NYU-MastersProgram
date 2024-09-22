#!/usr/bin/env python3

import time

start_time = time.time()

# The value we are trying to return from traverse()
target = 9595

# The integer values that can be added to our return value
numbers = [227, 505, 1128, 531, 289, 937, 410, 314, 866, 710]

# A dictionary where keys are the current integer (previously added integer) and the values are the integers that we can jump to next
numberswithpath = {
    227: [227, 1128, 410], 505: [505, 289, 531], 1128: [1128, 531, 410], 531: [531, 866, 531], 289: [289, 937, 314], 
    937: [937, 227, 937], 410: [410, 710, 227], 314: [314, 227, 710], 866: [866, 710, 505], 710: [710, 710, 531]
}

# Lists for storing possible solutions found during execution
possibleanswer = []
answer = []

# Function to find all combinations of our possible integer values that can be summed to equal our tatget value '9595'
# Source: https://stackoverflow.com/questions/20193555/finding-combinations-to-the-provided-sum-value
def subsets_with_sum(lst, target, with_replacement=False):
    x = 0 if with_replacement else 1
    def _a(idx, l, r, t):
        if t == sum(l): r.append(l)
        elif t < sum(l): return
        for u in range(idx, len(lst)):
            _a(u + x, l + [lst[u]], r, t)
        return r
    return _a(0, [], [], target)
all_sums = subsets_with_sum(numbers, target, True)
#print(len(x))

# Loop to refine our possible solutions to only include paths that start 227, this 
# first integer is always a given due to the nature of the program
for entry in all_sums:
    if entry[0] == 227:
        #possibleanswer.append(list(dict.fromkeys(entry)))
        possibleanswer.append(entry)
    else:
        continue

# Eliminate any duplicates from our list of possible paths
possibleanswer_nodup = []
[possibleanswer_nodup.append(n) for n in possibleanswer if n not in possibleanswer_nodup]

# Further reduce our list of possible paths to only include steps that are actually possible within the programs constraints
for i in possibleanswer_nodup:
    foo = 0
    for j in range(0, len(i)-1):
        if i[j+1] not in numberswithpath[i[j]]:
            foo = 1
    if foo == 0:
        answer.append(i)

# Print our the number of possible paths discovered, each path that met all of the above constraints, and the time needed to find these paths
print("Number of possible paths found: ", len(answer))
print("Possible paths: ")
for z in answer:
    print(z)
print("Execution Time: --- %s seconds ---" % (time.time() - start_time))