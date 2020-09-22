# 02_Analysis
This folder contains the scripts to generate the files used for the analysis. DESeq2 is used to generate a file for the
differential gene expression, TEPIC is used to calculate transcription factor affinity scors and DYNAMITE is used
to infer the key TFs.

## Content
### `DESeq2`
Count files and R-notebook containing the setup / usage for DESeq2

### `TEPIC`
Script to run TEPIC for a given list of histone modifications and time points.

### `DYNAMITE`
Script to generate the DYNAMITE.cfg for a given list of comparisons and histone markers.