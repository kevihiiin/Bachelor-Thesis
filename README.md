# Bachelor-Thesis
Code repository containing the scripts used for the analysis in my Bachelor Thesis 
`Machine Learning Based Gene Expression Prediction from ChIP-seq Signal in Lactation`.

The code in this repository can be divided into three sections:
+ Preprocessing of the datasets (ChIP-seq and RNA-seq) using nf-core[1]
+ Analysis of the data using DESeq2[2], TEPIC[3] and DYNAMITE[4]
+ Visualization and verification of the results 


## Preprocessing of the datasets
The data used to create the datasets first needs to be fetched using their GEO IDs.
Specifically, the raw NGS sequencing files need to be obtained. This download helper script can be found in
```
PA_Scripts/Download_Data
```
The files are then preprocessed using the nf-core ChIP-seq[5] and RNA-seq[6] pipeline. The ChIP-seq pipeline requires 
an input setup file, containing the paths to the sample and some metadata. A script to create all the files can be found in
```
Preprocessing
```

## Analysis of the data

## Visualization and verification of the results