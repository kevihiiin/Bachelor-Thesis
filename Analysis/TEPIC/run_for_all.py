from pathlib import Path

import numpy as np

from Analysis.affinity2bed.affinity2bed import convert_affinity_to_bed
from Analysis.TEPIC.calculate_auroc import calculate_auroc_score

time_points = ['L1', 'L10', 'p6', 'p13']
# time_points = ['L1']
hms = ['H3K27ac', 'H3K4me3']
# hms = ['H3K27me3', 'H3K4me1']

tepic_path = Path('/home/kevin/tmp/OUTPUT/TEPIC/')
output_path = Path('/home/kevin/tmp/OUTPUT/TEPIC/affinity_bed')
reference_path = Path('/home/kevin/tmp/OUTPUT/STAT5/')

result_string = ""

for time in time_points:
    for hm in hms:
        print(f'========== START ===========')
        # --- Convert affinities to bed files
        current_path = tepic_path.joinpath(time, hm)
        affinity_bed_folder_path = output_path.joinpath(time, hm)

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

with open('scores_2.txt', 'w') as result_file:
    result_file.write(result_string)
