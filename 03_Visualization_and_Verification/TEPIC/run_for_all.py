import argparse
from pathlib import Path

import numpy as np

from .affinity_to_bed import convert_affinity_to_bed
from .calculate_pr_auc import calculate_auroc_score

time_points = ['L1', 'L10', 'p6', 'p13']
hms = ['H3K27ac', 'H3K4me3']

# Argument parser
parser = argparse.ArgumentParser(description='Caclulate the PR-AUC scores for all of the TEPIC output')
parser.add_argument('--tepic-output', type=str, required=True, help="TEPIC output converted to bed file")
parser.add_argument('--reference', type=str, help="Folder containing the reference ChIP-seq files")
parser.add_argument('--tmp', type=str, default="/tmp", help="Temporary path to write the generated bed files to")

args = parser.parse_args()

# Config options
tepic_path = Path(args.tepic_output) # Path of the TEPIC output
reference_path = Path(args.reference) # Containing the narrowPeak file and _negative.bed files
tmp_path = Path(args.tmp) # Where to write the temporary affinity -> bed files

result_string = ""

for time in time_points:
    for hm in hms:
        print(f'========== START ===========')
        # --- Convert affinities to bed files
        current_path = tepic_path.joinpath(time, hm)
        affinity_bed_folder_path = tmp_path.joinpath(time, hm)

        # Convert affinity to bed
        run_conversion = False
        if run_conversion:
            affinity_bed_folder_path.mkdir(exist_ok=True, parents=True)

            # Convert affinities for all files
            for affinity_path in current_path.rglob('*_Affinity.txt'):
                convert_affinity_to_bed(input_file_path=affinity_path, output_path=affinity_bed_folder_path,
                                        tf_pattern='STAT5')

        # Obtain path for reference
        positive_set_path = reference_path.joinpath(time, next(reference_path.rglob('*.narrowPeak')))
        negative_set_path = reference_path.joinpath(time, next(reference_path.rglob('*_negative.bed')))

        # Calculate F1 score
        results_list = []
        for affinity_bed_path in affinity_bed_folder_path.rglob('*.bed'):
            result = calculate_auroc_score(sample_path=affinity_bed_path, positive_set_path=positive_set_path,
                                           negative_set_path=negative_set_path)
            results_list.append(result)

        print(f'Time: {time} | HM: {hm}')
        print(results_list)
        print(np.mean(results_list))
        print(np.std(results_list))

        result_string += f'Time: {time} | HM: {hm}\n'
        result_string += str(np.mean(results_list)) + '\n'
        result_string += "Std: " + str(np.std(results_list)) + '\n\n'

with open('result_scores.txt', 'w') as result_file:
    result_file.write(result_string)
