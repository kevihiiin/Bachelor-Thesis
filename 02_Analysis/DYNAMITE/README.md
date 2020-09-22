# DYNAMITE
Creates the DYNAMITE.cfg files for a given list of time point comparisons and histone modifications.
Execution of DYNAMITE must be started manually

## Content
### `setup_file_all.tsv`
Setup file containing time points to compare and histone modification. Timepoints must be written as 
\<time point\>\_vs\_\<time_point\>.

### `DYNAMITE-TEMPLATE.cfg`
Template for DYNAMITE.cfg in which the paths are inserted to.

### `setup_dynamite.py`
Generator script that takes the template and the setup file to generate the DYNAMITE.cfg config files.

Example:
```shell script
python setup_dynamite.py --dynamite <path_to_dynamite> --output <path_to_write_output_to>
``` 

Usage:
```
usage: setup_dynamite.py [-h] --dynamite DYNAMITE --output OUTPUT [--config CONFIG] [--template TEMPLATE]

DYNAMITE Setup generator

optional arguments:
  -h, --help           show this help message and exit
  --dynamite DYNAMITE  Dynamite path
  --output OUTPUT
  --config CONFIG
  --template TEMPLATE

```