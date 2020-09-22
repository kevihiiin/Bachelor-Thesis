#!/bin/bash
N=40

for filename in $(find . -type f -name "*.fastq.gz"); do
	((i=i%N)); ((i++==0)) && wait
	echo $(zcat $filename | sed '1~4d' - | md5sum - | cut -f 1 -d' ') $filename &
done
