# Bachelor-Thesis
Code repository containing the scripts used for the analysis in my Bachelor Thesis 
`Machine Learning Based Gene Expression Prediction from ChIP-seq Signal in Lactation`.

The code in this repository can be divided into three sections:
+ Preprocessing of the datasets (ChIP-seq and RNA-seq) using nf-core[1]
+ Analysis of the data using DESeq2[2], TEPIC[3] and DYNAMITE[4]
+ Visualization and verification of the results 


## Preprocessing of the datasets
[01_Preprocessing](01_Preprocessing) contains scripts used to:
+ Download all the raw fastq files from GEO IDs
+ Count the number of biological replicates
+ Check for duplicate files
+ Create the the input.csv needed for the nf-core/chip-seq pipeline

## Analysis of the data
[02_Analysis](02_Analysis) contains scripts used to:
+ Generate and visualize the output for DESeq2
+ Generate the output for TEPIC
+ Setup the configuration files for DYNAMITE

## Visualization and verification of the results
[03_Visualization_and_Verification](03_Vizualization_and_Verification) contains scripts to:
+ Verify the results of TEPIC (creating PR-AUC scores)
+ Visualize the results of DYNAMITE.