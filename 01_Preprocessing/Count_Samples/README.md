# Count_Samples
Counting the number of biological replicates (same time point and same histone marker) from the input table (the same 
one that was used to download the samples).

## Content
### `count_samples.py`
Used to generate a sample_count.xlsx sample count file.
Usage:
```shell script
python count_samples.py --input "../GEO data list.xlsx" --output "./Output"
```