import argparse
import re
import string
import pandas as pd

from pathlib import Path

# Argument parser
parser = argparse.ArgumentParser(description='TEPIC affinity to bed files converter')
parser.add_argument('--input', type=str, required=True, help="TEPIC _Affinity.txt input file path")
parser.add_argument('--filter', type=str, help="Pattern of TF name that will be extracted to bed files")
parser.add_argument('--scaling', default=1000, type=int, help="Scaling to apply to each TF affinity score")
parser.add_argument('--cutoff', default=1, type=int, help="Filter out regions where final score is smaller than cutoff")

args = parser.parse_args()

# Config options
input_file_path = Path(args.input)
tf_pattern = args.filter
tf_scaling = args.scaling
tf_cutoff = args.cutoff
# Print configuration
print(f'Processing input file: {input_file_path}')

# Get sample name
sample_name = '_'.join(input_file_path.name.split('_')[:2])
# Get and create output dir
output_path = input_file_path.parent.joinpath('bed_files')
output_path.mkdir(exist_ok=True)

# Parse input DataFrame
input_df = pd.read_table(input_file_path)
header_df = input_df.iloc[:, 0]  # Chromosome, start end
value_df = input_df.iloc[:, 1:]  # Peak value

position_df = pd.DataFrame()
position_df[['chr', 'start']] = header_df.str.split(':', expand=True)
position_df[['start', 'end']] = position_df.iloc[:, 0 - 1].str.split('-', expand=True).astype(int)

full_df = pd.concat([position_df, value_df], axis=1).sort_values(by=['chr', 'start'])

# Get the candidates (e.g. containing STAT)
if tf_pattern:
    p = re.compile(tf_pattern, re.IGNORECASE)
    tf_candidates = [x for x in full_df.columns if p.match(x)]
    print(f'The following TF candidates following the pattern "{tf_pattern}" were found:\n{tf_candidates}')
else:
    tf_candidates = full_df.columns[3:]
    print(f'No pattern was supplied. Extracting all TFs')


# Convert to bed files
def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.

Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.

Source: https://gist.github.com/seanh/93666

"""
    valid_chars = ":-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    filename = filename.replace(':', '-')  # I don't like spaces in filenames.
    return filename


for tf in tf_candidates:
    # Define output path
    output_file_path = output_path.joinpath(format_filename(tf) + '.bed')
    # Create output DataFrame
    output_df = full_df[['chr', 'start', 'end', tf]]
    # Apply scaling to TF affinity score
    output_df[tf] = output_df[tf] * tf_scaling
    # Add dummy columns
    output_df.insert(3, 'name', tf)
    output_df.insert(5, 'strand', '.')
    # Filter out values that are smaller than cutoff
    output_df = output_df.loc[output_df[tf] >= tf_cutoff]
    print(f'TF: {tf} | Min: {output_df[tf].min()} | Max: {output_df[tf].max()} | Mean: {output_df[tf].mean()}')
    print(f'Output file: {output_file_path}')
    output_df.to_csv(output_file_path, index=False, header=False, sep='\t')
