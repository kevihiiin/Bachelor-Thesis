#%%

import os
import re
import random
import string
import tqdm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

input_file_path = '/home/kevin/tmp/group1_hic/bed_files/WT_L1_STAT5_R12_peaks.narrowPeak'
output_dir = '/home/kevin/tmp/group1_hic/bed_files/reference'

# Parse input file as DataFrame
full_df = pd.read_table(input_file_path, names= ['chr', 'start', 'end', 'name', 'score', 'strand', 'signalValue', 'pValue', 'qValue', 'peak'])

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
n_peaks = pd.DataFrame({'chr': sorted_full_df['chr'], 'start': sorted_full_df['end'].shift(1), 'end': sorted_full_df['start']}).dropna()
n_output_df = pd.DataFrame(columns=['chr','start','end','name','score','strand'])

np.random.seed(1)
random.seed(1)

peak_length_random = np.random.normal(loc = peak_mean, scale = 500, size = int(len(p_peaks)*1000)).astype(int)
peak_length_random = peak_length_random[peak_length_random > 10]
print(f'RANDOM {peak_length_random}')
print(f'RANDOM min {peak_length_random.min()}')
print(f'RANDOM max {peak_length_random.max()}')
counter = 0
for index, row in tqdm.tqdm(n_peaks.iterrows(), total=n_peaks.shape[0]):
    gap_length = row['end'] - row['start']
    peak_length = 0

    # Get peak length smaller than gap
    for _ in range(1000):
        peak_length = peak_length_random[counter]
        counter += 1
        if peak_length <= gap_length:
            break

    # Get start offset
    offset = 0
    try:
        offset = random.randint(0, int(gap_length - peak_length))
    except ValueError:
        continue

    # Add row to df
    row_start = row['start'] + offset

    n_output_df.loc[index] = [row['chr'], row_start, row_start + peak_length, 'n_peak', 1, '.']

# No digits
n_output_df[["start", "end"]] = n_output_df[["start", "end"]].astype(int)
# Sort
n_output_df = n_output_df.sort_values(['chr', 'start'])

print(f"MEAN {(n_output_df['end'] - n_output_df['start']).mean()}")
print(f"Length {len(n_output_df['start'])}")
n_output_df.to_csv(os.path.join(output_dir, 'negative_peak.bed'), index=False, header=False, sep='\t')
