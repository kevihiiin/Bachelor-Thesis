import argparse
from pathlib import Path

import pandas as pd
import numpy as np


# Argument parser
parser = argparse.ArgumentParser(description='Script to generate the input csv file for the nf-core/chip-seq pipeline.')
parser.add_argument('--input', type=str, required=True, help="Path to the GEO data list.xlsx excel sheet")
parser.add_argument('--output', type=str, required=True, help="Path to write the sample_count.xlsx to")
parser.add_argument('--time-stamp', type=str, required=True, help="Time stamp of the samples that should be used")

args = parser.parse_args()

# Config options
input_xlsx_path = Path(args.input)
output_path = Path(args.output)
time_stamp = args.time_stamp

group_prefix = f'WT_{time_stamp}'
output_csv_path = output_path.joinpath(f'{time_stamp}_input.csv')
fastq_path = '/nfs/data/Hennighausen/01_raw/chipseq'


# --- Parse excel file into dataframe
input_df = pd.read_excel(input_xlsx_path, index_col=[0]).dropna(axis=0, how='all')

# --- Keep only files with timestamp of interest
input_df = input_df[input_df['time stamp'] == time_stamp]
chip_seq_df = input_df[input_df['experiment type'] == 'ChIP-Seq']
control_df = input_df[input_df['experiment type'] == 'Control']

# --- Create output dataframe
output_df = pd.DataFrame()
row_names = ['group', 'replicate', 'fastq_1', 'fastq_2', 'antibody', 'control']

# -- ChIP-seq data
# Filter out 'duplicates' / 'x'
chip_seq_df = chip_seq_df[~chip_seq_df['notes'].isin(['DUPLICATE', 'x'])]
# Lambda function for populating
chip_seq_lamdafunc = lambda x: pd.Series([f"{group_prefix}_{x['antibody'].split('-')[0]}",
                                          np.nan,
                                          f"{fastq_path}/{time_stamp}/{x['file name'].strip()}.fastq.gz",
                                          np.nan,
                                          x['antibody'].split('-')[0],
                                          f"{group_prefix}_CONTROL"])
# Populate dataframe
output_df[row_names] = chip_seq_df.apply(chip_seq_lamdafunc, axis=1)
output_df = output_df.sort_values('antibody')

# -- Control data
# Filter out 'duplicates' / 'x'
control_df = control_df[control_df['notes'].isin(['use'])]
# Lambda function for populating
control_seq_lamdafunc = lambda x: pd.Series([f"{group_prefix}_CONTROL",
                                             np.nan,
                                             f"{fastq_path}/controls/{time_stamp}/{x['file name'].strip()}.fastq.gz",
                                             np.nan,
                                             np.nan,
                                             np.nan])
# Populate dataframe
output_control_df = pd.DataFrame()
output_control_df[row_names] = control_df.apply(control_seq_lamdafunc, axis=1)
output_df = pd.concat([output_df, output_control_df])
print(output_df)

output_df.to_csv(output_csv_path, index=False)
