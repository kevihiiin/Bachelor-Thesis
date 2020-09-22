#!/bin/bash
N=1

for filename in $(find . -type f -name "*.fastq.gz"); do
	((i=i%N)); ((i++==0)) && wait
	echo $(zcat $filename | head -2 | tail -1) $filename &
done
