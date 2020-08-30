import pandas as pd

input_file_path = '/home/kevin/tmp/group1/WT_L1_H3K4me3_R3_peaks.narrowPeak_TEPIC_08_04_20_12_29_53_559767100_Affinity.txt'

input_df = pd.read_table(input_file_path)

print(input_df)
