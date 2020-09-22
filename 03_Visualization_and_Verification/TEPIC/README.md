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

Example:
```shell script
python affinity_to_bed.py --input <*_Affinity.txt> --output <directory_to_write_bed_files_to
```

Usage:
```
usage: affinity_to_bed.py [-h] --input INPUT [--output OUTPUT] [--filter FILTER] [--scaling SCALING] [--cutoff CUTOFF]

TEPIC affinity to bed files converter

optional arguments:
  -h, --help         show this help message and exit
  --input INPUT      TEPIC _Affinity.txt input file path
  --output OUTPUT    Output folder to write the bed files to
  --filter FILTER    Pattern of TF name that will be extracted to bed files
  --scaling SCALING  Scaling to apply to each TF affinity score
  --cutoff CUTOFF    Filter out regions where final score is smaller than cutoff

```

### `bed_to_negativebed`
Script used to generate the "negative peaks" from a given peak / bed / narrowPeak file.

Example:
```shell script
python bed_to_negativebed.py --input <narrowPeak_file> --output <output_directory_where_files_are written>
```

Usage:
```
usage: bed_to_negativebed.py [-h] --input INPUT [--reference REFERENCE] --output OUTPUT

Calculates peaks in negative space of bed file "negative peaks"

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Bed file containing "positive peaks"
  --reference REFERENCE
                        Reference bed file containing all regions in genome
  --output OUTPUT       Output directory where "negative peaks" are written to

```

### `calculate_pr-auc.py`
Calculates the PR-AUC for the predicted TEPIC affinity scores converted to bed files (output of affinity_to_bed) for 
a give gold standard with negative peaks (output of bed_to_negativebed).

Example:
```shell script
python calculate_pr-auc.py --sample <tepic_affinity_bed_file> --positive-ref <narrowPeak_file> --negative-ref <negative_bed_file>
```

Usage:
```
usage: calculate_pr_auc.py [-h] --sample SAMPLE [--positive-ref POSITIVE_REF] [--negative-ref NEGATIVE_REF]

Caclulate the PR-AUC scores for TEPIC output

optional arguments:
  -h, --help            show this help message and exit
  --sample SAMPLE       TEPIC output converted to bed file
  --positive-ref POSITIVE_REF
                        Bed file containing the positive peaks
  --negative-ref NEGATIVE_REF
                        Bed file for negative peaks, output of bed_to_negative

```

### `run_for_all.py`
Runs `calculate_pr-auc.py` for all samples. Please change the the used time points and histone markers inside the script.

Example:
```shell script
python run_for_all.py --tepic-output <path_to_tepic_output_folder> --reference <path_to_reference_files>
```

Usage:
```
usage: run_for_all.py [-h] --tepic-output TEPIC_OUTPUT [--reference REFERENCE] [--tmp TMP]

Caclulate the PR-AUC scores for all of the TEPIC output

optional arguments:
  -h, --help            show this help message and exit
  --tepic-output TEPIC_OUTPUT
                        TEPIC output converted to bed file
  --reference REFERENCE
                        Folder containing the reference ChIP-seq files
  --tmp TMP             Temporary path to write the generated bed files to

```
 