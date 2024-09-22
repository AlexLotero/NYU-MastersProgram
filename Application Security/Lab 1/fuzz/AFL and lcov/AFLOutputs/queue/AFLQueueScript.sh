#!/bin/bash

gcc -g --coverage giftcardreadercrash.c -o gcrcrash 

./gcrcrash 

./gcrcrash 1 crash2.gft

./gcrcrash 1 hang.gft

./gcrcrash 1 cov1.gft

./gcrcrash 2 cov2.gft

FILES=id*

for file in $FILES; do
	./gcrcrash 1 $file
	echo $file
done

lcov -c -d . -o gcrcrash.info

genhtml gcrcrash.info -o gcrcrash_report

exit
