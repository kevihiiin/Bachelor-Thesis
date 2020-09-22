# TEPIC
Run TEPIC for a given list of possible combinations on histone modifications and time points.

## Content
### `input_files`
Contains tab separated files with: time point<tab>histone modification
### `run_tepic.sh`
Script to run TEPIC for the combinations specified in `ìnput_files`.

Hint: Replace the paths to the reference files inside the script to your paths.

Usage:
```shell script
bash run_tepic.sh -s input_files/all_hm.tsv
```
