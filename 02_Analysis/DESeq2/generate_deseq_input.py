import pandas as pd
import pathlib
import re


group_1 = 'Lactation' # case
group_2 = 'Pregnancy' # control / base / earlier

output_path = pathlib.Path('output')

gene_id_path = 'Gene_id.txt'

# Read all count per group files into list
def read_count_files(group):
    count_file_path = pathlib.Path('count_files').joinpath(group)
    group_dict = dict()
    for count_file in count_file_path.glob('*-count.txt'):
        count_path = str(count_file)
        sample_name = re.match(r'.*\/(.*?)-count.txt', count_path).group(1)
        group_dict[sample_name] = pd.read_table(count_path)
    
    return [x[1] for x in sorted(group_dict.items())]

group_1_list = read_count_files(group_1)
group_2_list = read_count_files(group_2)

# Create Dataframe
gene_id_df = pd.read_table(gene_id_path)
output_df = pd.concat([gene_id_df] + group_1_list + group_2_list, axis=1)

# Write output matrix file
out_filename = f'{group_1}_vs_{group_2}.tsv'
output_df.to_csv(output_path.joinpath(out_filename), index=False, sep='\t', header=True)

# Write command file
sample_string = ', '.join(f'"{x}"' for x in output_df.columns[1:])
group_string = ', '.join([f'"{group_1}"' for x in group_1_list] + [f'"{group_2}"' for x in group_2_list])
with open(output_path.joinpath(f'{group_1}_vs_{group_2}_command.txt'), 'w') as outfile:
    outfile.write(f'metadata_df = data.frame(sample_id = c({sample_string}), group = c({group_string}))\n')