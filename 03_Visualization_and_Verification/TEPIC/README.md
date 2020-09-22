# TEPIC
Create PR-AUC scores for the predicted TEPIC results.
Steps needed to be perfomed:
+ Convert the affinity scores from TEPIC into bed files
+ Create "negative peaks" for the control sample
+ Calculate the PR-AUC scores

## Content
### `affinity_to_bed.py`
Script to convert the affinity files created by TEPIC for regions into bed files.
It allows for:
+ Filtering of the generated bed files for certain TFs, e.g. to only generated the bed files for STAT5. 
+ Scaling of the affinity scores into peaks (e.g. scaling factor of 1000).
+ Filtering of the score, so only peaks above the cutoff are shown.

Usage:
```shell script
python affinity_to_bed.py --input <*_Affinity.txt> --output <directory_to_write_bed_files_to
```
For more options print help:
```shell script
python affinity_to_bed.py --help
```

### `bed_to_negativebed`
Script used to generate the "negative peaks" from a given peak / bed / narrowPeak file.

Usage:
```shell script
python bed_to_negativebed.py --input <narrowPeak_file> --output <output_directory_where_files_are written>
```

### `calculate_pr-auc.py`
Calculates the PR-AUC for the predicted TEPIC affinity scores converted to bed files (output of affinity_to_bed) for 
a give gold standard with negative peaks (output of bed_to_negativebed).

Usage:
```shell script
python calculate_pr-auc.py --sample <tepic_affinity_bed_file> --positive-ref <narrowPeak_file> --negative-ref <negative_bed_file>
```

### `run_for_all.py`
Runs `calculate_pr-auc.py` for all samples. Please change the the used time points and histone markers inside the script.

Usage:
```shell script
python run_for_all.py --tepic-output <path_to_tepic_output_folder> --reference <path_to_reference_files>
```
 