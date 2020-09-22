# Count_Samples
Counting the number of biological replicates (same time point and same histone marker) from the input table (the same 
one that was used to download the samples).

## Content
### `count_samples.py`
Used to generate a sample_count.xlsx sample count file.

Example:
```shell script
python count_samples.py --input "../GEO data list.xlsx" --output "./Output"
```

Usage:
```
usage: count_samples.py [-h] --input INPUT --output OUTPUT

Script to count the number of biological replicates

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    Path to the GEO data list.xlsx excel sheet
  --output OUTPUT  Path to write the sample_count.xlsx to

```