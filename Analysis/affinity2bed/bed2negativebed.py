# %%

import os
import random
import pybedtools
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
from ortools.linear_solver import pywraplp
from scipy import stats


input_file_path = '/home/kevin/tmp/TRASH/WT_L1_STAT5_R5_peaks.narrowPeak'
output_path = Path('/home/kevin/tmp/TRASH/negative_bed/')

# Parse input file as DataFrame
full_df = pd.read_table(input_file_path,
                        names=['chr', 'start', 'end', 'name', 'score', 'strand', 'signalValue', 'pValue', 'qValue',
                               'peak'])

# Create negative peaks
# Sort DF
sorted_full_df = full_df
sorted_full_df[['start', 'end']] = sorted_full_df[['start', 'end']].astype(int)
sorted_full_df = sorted_full_df.sort_values('start')

# Calculate mean of peak width
p_peaks = sorted_full_df['end'] - sorted_full_df['start']
peak_mean = p_peaks.mean()
peak_count = sorted_full_df.shape[1]
print(f'Positive peak mean: {peak_mean}')
print(f'Positive peak min: {p_peaks.min()}')
print(f'Positive peak max: {p_peaks.max()}')

# Calculate negative space
n_peaks = pd.DataFrame(
    {'chr': sorted_full_df['chr'], 'start': sorted_full_df['end'].shift(1), 'end': sorted_full_df['start']}).dropna()
n_output_df = pd.DataFrame(columns=['chr', 'start', 'end', 'name', 'score', 'strand'])

# Permute rows
# _ = n_peaks.iloc[np.random.permutation(np.arange(len(n_peaks)))]

# Remove overlapping regions
overlap_count = len(n_output_df)
while True:
    old_len = len(n_output_df)
    n_output_df = n_output_df[n_output_df['start'] - n_output_df['end'].shift(1, fill_value=0) >= 0]

    if old_len == len(n_output_df):
        break

print(f'Removed {overlap_count - len(n_output_df)} overlaps')

# --- Create random peaks
parameters = stats.lognorm.fit(p_peaks, loc=0)
random_peaks = stats.lognorm.rvs(parameters[0], parameters[1], parameters[2], size=len(p_peaks)).astype(int)

sns.distplot(p_peaks)
sns.distplot(random_peaks)
plt.savefig(output_path.joinpath('distplot.svg'))
# --- Find an optimal packing
n_peaks['bin'] = n_peaks['end'] - n_peaks['start']

#
min_random = random_peaks.min()
n_peaks = n_peaks[n_peaks['bin'] > min_random].sort_values(['bin'])


"""
for split in np.array_split(n_peaks, int(len(n_peaks) / 100)):
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
    print('Add variables to bin')
    x = {}
    for i in tqdm(data['items']):
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    print('Add constraints placed once')
    for i in tqdm(data['items']):
        solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    print('Add constraints max capacity')
    for j in tqdm(data['bins']):
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    print('Start solver')
    status = solver.Solve()
    print('Finished solving')

    total_weight = 0
    for j in data['bins']:
        bin_weight = 0
        bin_value = 0
        print('Bin ', j, '\n')
        for i in data['items']:
            if x[i, j].solution_value() > 0:
                print('Item', i, '- weight:', data['weights'][i], ' value:',
                      data['values'][i])
                bin_weight += data['weights'][i]
                bin_value += data['values'][i]
        print('Packed bin weight:', bin_weight)
        print('Packed bin value:', bin_value)
        print()
        total_weight += bin_weight

    print('Total packed value:', objective.Value())
    print('Total packed weight:', total_weight)
"""

# # No digits
# n_output_df[["start", "end"]] = n_output_df[["start", "end"]].astype(int)
# # Sort
# n_output_df = n_output_df.sort_values(['chr', 'start'])
#
# print(f"MEAN {(n_output_df['end'] - n_output_df['start']).mean()}")
# print(f"Length {len(n_output_df['start'])}")
# n_output_df.to_csv(os.path.join(output_dir, 'negative_peak.bed'), index=False, header=False, sep='\t')
