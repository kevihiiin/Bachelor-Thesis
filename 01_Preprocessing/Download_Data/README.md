# Download_Data
Scripts used to download raw fastq files from a list of given GEO accession IDs. 
The script first fetches the SRA run IDs from the given GEO IDs and the uses the ENA mirror of the SRA to download all 
the files (ENA is faster than the SRA). Uses aspera for downloading, the script can be easily changed to use FTP instead.

## Content
### `GEO data list.csv`
Table containing the GEO IDs and file name of the files to download.

### `Download_fastq_from_geo.py`
Script to download all the data from ENA given GEO IDs. Creates a temporary <input_file_csv>.tmp file, from which it 
can resume downloading.

Example:
```shell script
python Download_fastq_from_geo.py --input "GEO data list.csv" [--resume] \ # Add --resume to resume downloading
      [--ssh-key-file "<path to the ssh-key files generated by the aspera client>]"
```

Usage:
```
usage: Download_fastq_from_geo.py [-h] --input INPUT --output OUTPUT [--resume] [--ssh-key-file SSH_KEY_FILE]

Download fastq files from a given list of GEO IDs

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Path to the input csv file
  --output OUTPUT       Path to write the downloaded samples to
  --resume              If specified resume downloading
  --ssh-key-file SSH_KEY_FILE
                        Path to the ssh key file used by the aspera client

```