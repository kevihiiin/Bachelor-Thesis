# nf-core_generator
Script used to generate the input csv file containing the ChIP-seq fastq files for the nf-core/chip-seq pipeline.

## Content
### `create_nexflow_input.py`
Usage:
```shell script
python create_nexflow_input.py --input "../GEO data list.xlsx" --output "./output" --time-stamp p6 # Can be any time stamp
```