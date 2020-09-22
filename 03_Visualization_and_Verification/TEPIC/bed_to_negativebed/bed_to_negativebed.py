import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pybedtools
import seaborn as sns
from ortools.linear_solver import pywraplp
from scipy import stats
from tqdm import tqdm

# Argument parser
parser = argparse.ArgumentParser(description='Calculates peaks in negative space of bed file "negative peaks"')
parser.add_argument('--input', type=str, required=True, help='Bed file containing "positive peaks"')
parser.add_argument('--reference', type=str, default='chmm38_full_peak.bed',
                    help='Reference bed file containing all regions in genome')
parser.add_argument('--output', type=str, required=True, help='Output directory where "negative peaks" are written to')

args = parser.parse_args()

# Options
input_bed_path = Path(args.input)
reference_bed_path = Path(args.reference)
output_path = Path(args.output)
outfile_prefix = input_bed_path.stem # Filename prefix

# --- Parse input files
# Parse ChIP-seq input file as DataFrame
chip_df = pd.read_table(input_bed_path,
                        names=['chr', 'start', 'end', 'name', 'score', 'strand', 'signalValue', 'pValue', 'qValue',
                               'peak'])

# Create and parse negative space .bed file as DataFrame
reference_bed = pybedtools.BedTool(reference_bed_path)
n_space_df = reference_bed.subtract(str(input_bed_path)).to_dataframe()

# --- Peaks handling
# Get peaks from ChIP-seq file
p_peaks = chip_df['end'] - chip_df['start'] - 1
print('--- Positive Peaks ---')
print(f'Positive peak mean: {p_peaks.mean()}')
print(f'Positive peak min: {p_peaks.min()}')
print(f'Positive peak max: {p_peaks.max()}')
print()

# Create random peaks for negative space
parameters = stats.lognorm.fit(p_peaks, loc=0)
random_peaks = stats.lognorm.rvs(parameters[0], parameters[1], parameters[2], size=len(p_peaks)+500).astype(int)
print('--- Negative Peaks ---')
print(f'Negative peak mean: {random_peaks.mean()}')
print(f'Negative peak min: {random_peaks.min()}')
print(f'Negative peak max: {random_peaks.max()}')
print()
random_peaks_sum = random_peaks.sum()

sns.distplot(p_peaks)
sns.distplot(random_peaks)
plt.savefig(output_path.joinpath(f'{outfile_prefix}_distplot.svg'))

# --- Find an optimal packing
n_space_df['bin'] = n_space_df['end'] - n_space_df['start'] - 1

min_random = random_peaks.min()
n_peaks = n_space_df[n_space_df['bin'] > min_random]
random_peaks = list(random_peaks)
total_weight = 0
total_value = 0

bed_file_header = ['chrom', 'start', 'end']
output_df = pd.DataFrame(columns=bed_file_header)

rng = np.random.default_rng()

# Fitting negative peaks
print('--- Fitting negtive peaks ---')
for split in tqdm(np.array_split(n_peaks, int(len(n_peaks) / 200))):
    split.reset_index(drop=True, inplace=True)
    tmp_peak_count = len(split)

    # Create data object
    data = {
        # Bins
        'bins': list(range(tmp_peak_count)),
        'bin_capacities': list(split['bin']),
        # Items
        'weights': [random_peaks.pop(0) + 1 for x in range(tmp_peak_count)],
        'values': [1] * tmp_peak_count,
        'items': list(range(tmp_peak_count)),
    }

    # Create solver and solve
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver.CreateSolver('multiple_knapsack_mip', 'CBC')

    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    # print('Add variables to bin')
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    # print('Add constraints placed once')
    for i in data['items']:
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    # print('Add constraints max capacity')
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    # print('Start solver')
    status = solver.Solve()
    # print('Finished solving')

    # Get the result and write back to DF
    results_dict = {
        'chrom': [],
        'start': [],
        'end': [],
    }  # Dict with lists as columns with all peaks and location
    for j in data['bins']:
        bin_weight = 0
        peaks_list = []  # Holds a list with all the peak lengths for this bin
        for i in data['items']:
            if x[i, j].solution_value() > 0:
                peak_size = data['weights'][i] - 1
                peaks_list.append(peak_size)
                bin_weight += peak_size

        total_weight += bin_weight
        # No peaks in this bin, go to next bin
        if len(peaks_list) == 0:
            continue

        # Calculate spacing
        empty_space = data['bin_capacities'][j] - bin_weight + 1
        if empty_space > 1:
            random_integers = np.append(rng.integers(low=1, high=empty_space, size=len(peaks_list)), [0, empty_space])
            random_integers.sort()
            spacing_array = np.diff(random_integers)
        else:
            spacing_array = rng.integers(2)

        # Create the peak rows
        chrom = split.iloc[j]['chrom']
        start = split.iloc[j]['start']
        gap_end = split.iloc[j]['end']

        for index, peak in enumerate(peaks_list):
            start += spacing_array[index]
            end = start + peak

            results_dict['chrom'].append(chrom)
            results_dict['start'].append(start)
            results_dict['end'].append(end)

            start = end
    tmp_df = pd.DataFrame.from_dict(results_dict)
    # print(tmp_df)
    output_df = output_df.append(tmp_df)
    total_value += objective.Value()
    # print('Total packed value:', objective.Value())
print(f'Total packed value: {total_value} | of {len(n_peaks)}')
print(f'Total packed weight: {total_weight} | of {random_peaks_sum}')
print()

output_df['name'] = 'negative_peak'

print('--- Writing output file ---')
print(output_df)
output_df.to_csv(output_path.joinpath(f'{outfile_prefix}_negative.bed'), index=False, header=False, sep="\t")
