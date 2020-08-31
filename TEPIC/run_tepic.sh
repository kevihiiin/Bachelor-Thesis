#!/bin/env bash
set -e  # Exit script on error
set -x  # Print every exectued line, nice for debugging

hic=False

# === Configuration ===
# General configuration
sample_list="/home/kevin/Uni/Bachelor-Thesis/TEPIC/test.tsv"
input_folder="/home/kevin/tmp/TEPIC/_FILES"
output_folder="/home/kevin/tmp/TRASH"

# TEPIC Configuration
tepic_path="/home/kevin/tmp/TEPIC"
referenceGenome="/home/kevin/tmp/TEPIC/_FILES/genome.fa"
geneAnnotation="/home/kevin/tmp/TEPIC/_FILES/gencode.vM25.annotation.gtf"
pwm="/home/kevin/tmp/TEPIC/PWMs/2.1/Merged_PSEMs/Merged_JASPAR_HOCOMOCO_KELLIS_Mus_musculus.PSEM"
decay="TRUE"
window=50000
cores_TEPIC=8

while read -r time_point histone_mark; do

	# Create folder structure
	output_path=${output_folder}/${time_point}/${histone_mark}
	mkdir -p $output_path

	# Iterate over every file for histone mark
	for bed_file in ${input_folder}/*${histone_mark}*.narrowPeak; do
		# Get output file prefix, aka ${histone_mark}_R[0-9]
		output_prefix=$(basename $bed_file | sed -e "s/^WT_${time_point}_//" -e "s/_peaks.narrowPeak$//")
		output=${output_path}/${output_prefix}

		# Execute TEPIC
		bash ${tepic_path}/Code/TEPIC.sh -g $referenceGenome -b $bed_file -o $output -p $pwm -c $cores_TEPIC -w $window -a $geneAnnotation -f $geneAnnotation -e $decay
	done
done < $sample_list
