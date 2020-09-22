import argparse
from pathlib import Path

import pandas as pd

# Argument parser
parser = argparse.ArgumentParser(description='Script to count the number of biological replicates')
parser.add_argument('--input', type=str, required=True, help="Path to the GEO data list.xlsx excel sheet")
parser.add_argument('--output', type=str, required=True, help="Path to write the sample_count.xlsx to")

args = parser.parse_args()

# Config options
csv_path = Path(args.input)
output_path = Path(args.output)

df = pd.read_excel(csv_path, index_col=[0]).dropna(axis=0, how='all')

# Keep only ChIP-Seq experiments, take only 'time stamp' and 'antibody' column
rna_seq = df[df['experiment type'] == 'RNA-Seq'][['experiment type', 'time stamp']]
print(rna_seq.groupby('time stamp').count())
count_df = df[df['experiment type'] == 'ChIP-Seq'][['time stamp', 'antibody']]

# Remove everything after dash in antibody column
count_df['antibody'] = count_df['antibody'].str.split('-').str[0]

count_df = count_df.groupby(['time stamp', 'antibody']).size()

count_df.to_excel(output_path, sheet_name='Count_Table')

print(count_df)
