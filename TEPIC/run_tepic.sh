#!/usr/bin/env bash
set -e  # Exit script on error
set -x  # Print every exectued line, nice for debugging

while getopts s:h: flag
do
    case "${flag}" in
        s) sample_list=${OPTARG};;
	h) hic=TRUE
    esac
done

# === Configuration ===
# General configuration
input_folder="/nfs/home/users/kyuan/Hennighausen/02_chipseq"
output_folder="/nfs/home/users/kyuan/Output/TEPIC"

# TEPIC Configuration
tepic_path="/nfs/home/users/kyuan/TEPIC"
referenceGenome="/nfs/home/users/kyuan/references/genome.fa"
geneAnnotation="/nfs/home/users/kyuan/references/gencode.vM25.annotation.gtf"
pwm="${tepic_path}/PWMs/2.1/Merged_PSEMs/Merged_JASPAR_HOCOMOCO_KELLIS_Mus_musculus.PSEM"
decay="TRUE"
window=50000
cores_TEPIC=80

while read -r time_point histone_mark; do
	# Create input path
	input_path=${input_folder}/${time_point}/bwa/mergedLibrary/macs/narrowPeak
	# Create folder structure
	output_path=${output_folder}/${time_point}/${histone_mark}
	mkdir -p $output_path

	# Iterate over every file for histone mark
	for bed_file in ${input_path}/*${histone_mark}*.narrowPeak; do
		# Get output file prefix, aka ${histone_mark}_R[0-9]
		output_prefix=$(basename $bed_file | sed -e "s/^WT_${time_point}_//" -e "s/_peaks.narrowPeak$//")
		output=${output_path}/${output_prefix}

		# Execute TEPIC
		bash ${tepic_path}/Code/TEPIC.sh -g $referenceGenome -b $bed_file -o $output -p $pwm -c $cores_TEPIC -w $window -a $geneAnnotation -f $geneAnnotation -e $decay
	done
done < $sample_list
