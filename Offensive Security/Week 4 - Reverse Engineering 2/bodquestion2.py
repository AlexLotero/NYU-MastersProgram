#!/usr/bin/env python3

import sys, resource

def recurse(a, b, c):
	x = b + (c - b) / 2
	print("x is: ", type(x))
	print("a is: ",  type(a))
	if (a < x):
		y = recurse(a, b, x -1)
		x = x + y
	elif (a > x):
		y = recurse(a, x + 1, c)
		x = x + y
	return x

def question2(a, b):
	c = recurse(a, 0, 0x14)
	return b != c

for i in range(0, 100):
	for j in range(0, 100):
		if i == j:
			continue
		z = question2(i, j)
		if z != 0:
			continue
		else:
			print("Correct value for i: ", i)
			print("Correct value for j: ", j)
			exit()

