# 01_Preprocessing
Contains scrips and files used for the preprocessing steps.

## Content
### `Downlaod_Data`
Scripts to download the raw fastq files from a given list of GEO IDs. 

### `Count_Samples`
Scripts and output to counts the number of biological replicates in the dataset.

### `Datasets`
Scripts and information generated to look for duplicated sequences in the dataset.

### `nf-core_generator`
Scripts used to generated the sample-matrix used as an input for the nf-core/chip-seq pipeline.

### `GEO data list.xlsx`
File containing information about all the samples used in the analysis. Contains files names as well as information 
about time stamp (e.g. L1, P13, I10), experiment type (ChIP-seq, RNA-Seq), antibody (for ChIP-seq only) and comments
on the file (use as control, duplicated, etc.).

