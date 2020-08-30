import pandas as pd

csv_path = "GEO data list.xlsx"

df = pd.read_excel(csv_path, index_col=[0]).dropna(axis=0, how='all')

# Keep only ChIP-Seq experiments, take only 'time stamp' and 'antibody' column
rna_seq = df[df['experiment type'] == 'RNA-Seq'][['experiment type', 'time stamp']]
print(rna_seq.groupby('time stamp').count())
count_df = df[df['experiment type'] == 'ChIP-Seq'][['time stamp', 'antibody']]

# Remove everything after dash in antibody column
count_df['antibody'] = count_df['antibody'].str.split('-').str[0]

count_df = count_df.groupby(['time stamp', 'antibody']).size()

count_df.to_excel('sample_count.xlsx', sheet_name='Count_Table')

print(count_df)
