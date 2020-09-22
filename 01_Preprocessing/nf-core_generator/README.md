# nf-core_generator
Script used to generate the input csv file containing the ChIP-seq fastq files for the nf-core/chip-seq pipeline.

## Content
### `create_nexflow_input.py`
Example:
```shell script
python create_nexflow_input.py --input "../GEO data list.xlsx" --output "./output" --time-stamp p6 # Can be any time stamp
```

Usage:
```
usage: create_nexflow_input.py [-h] --input INPUT --output OUTPUT --time-stamp TIME_STAMP

Script to generate the input csv file for the nf-core/chip-seq pipeline.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Path to the GEO data list.xlsx excel sheet
  --output OUTPUT       Path to write the sample_count.xlsx to
  --time-stamp TIME_STAMP
                        Time stamp of the samples that should be used

```