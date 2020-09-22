import argparse
from pathlib import Path

import pybedtools
import pandas as pd
from sklearn.metrics import roc_auc_score


def calculate_auroc_score(sample_path, positive_set_path, negative_set_path):
    sample = pybedtools.BedTool(sample_path)
    positive_set = pybedtools.BedTool(positive_set_path)
    negative_set = pybedtools.BedTool(negative_set_path)

    output_df = pd.DataFrame(columns=['score', 'label'])

    # # --- Determine all TP and FP
    sample_positive_overlap = sample.intersect(positive_set, c=True).to_dataframe()
    output_df['label'] = sample_positive_overlap.iloc[:, -1].astype(bool)
    output_df['score'] = sample_positive_overlap['score']

    # --- Determine all TN
    negative_sample_overlap = negative_set.intersect(sample, c=True).to_dataframe()
    negative_sample_overlap = negative_sample_overlap[negative_sample_overlap.iloc[:, -1] == 0]
    # Remove all the overlapping ones
    negative_sample_overlap['score'] = 0
    negative_sample_overlap['label'] = False
    output_df = output_df.append(negative_sample_overlap)

    # --- Determine all FN
    positive_sample_overlap = positive_set.intersect(sample, c=True).to_dataframe()
    # Get all non overlapping samples
    positive_sample_overlap = positive_sample_overlap[positive_sample_overlap.iloc[:, -1] == 0]
    # Set score to zero and label to True
    positive_sample_overlap['score'] = 0
    positive_sample_overlap['label'] = True
    output_df = output_df.append(positive_sample_overlap)

    result = roc_auc_score(output_df['label'], output_df['score'])
    return result

if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description='Caclulate the PR-AUC scores for TEPIC output')
    parser.add_argument('--sample', type=str, required=True, help="TEPIC output converted to bed file")
    parser.add_argument('--positive-ref', type=str, help="Bed file containing the positive peaks")
    parser.add_argument('--negative-ref', type=str, help="Bed file for negative peaks, output of bed_to_negative")

    args = parser.parse_args()

    # Config options
    sample_path = Path(args.sample)
    positive_set_path = Path(args.positive_ref)
    negative_set_path = Path(args.negative_ref)

    score = calculate_auroc_score(sample_path, positive_set_path, negative_set_path)
    print(score)
