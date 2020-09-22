#! /usr/bin/env python3
import argparse
import re
import subprocess
from pathlib import Path

import requests
import pandas as pd
import numpy as np

# Inspired by
# https://github.com/wwood/ena-fast-download/blob/master/ena-fast-download.py

# --- Constants ---
accession_path = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={}&targ=self&form=text&view=brief'

def geo_id_to_srx_ids(geo_id):
    result = requests.get(accession_path.format(geo_id))

    # If request was unsuccessful stop
    if result.status_code != 200:
        raise RuntimeError

    id_text = result.content.decode('UTF-8')

    srx_id_list = [x.strip() for x in re.findall(r'!Sample_relation = SRA: .*?=(SRX.*)', id_text)]

    return srx_id_list


def download_run(run_id, output_path, file_name, ssh_key_path):
    result_json = requests.get(
        f'https://www.ebi.ac.uk/ena/portal/api/filereport?accession={run_id}&download=false&fields=fastq_aspera%2Cfastq_md5&format=json&result=read_run').json()

    for single_run in result_json:
        fastq_aspera_path_list = single_run['fastq_aspera'].split(';')
        fastq_md5checksum_list = single_run['fastq_md5'].split(';')
        
        for fastq_aspera_path, fastq_md5checksum in zip(fastq_aspera_path_list, fastq_md5checksum_list):
            fastq_file_name = Path(fastq_aspera_path).name
            print(f'Download file {fastq_file_name}')

            cmd = "ascp -QT -l 500m -P33001 {} -i {} era-fasp@{} {}".format(
                "",  # Additional args
                ssh_key_path,
                fastq_aspera_path,
                output_path)

            process = subprocess.check_call(cmd, stdout=subprocess.PIPE, shell=True)

            print(f'Retval: {process}')

            # Check md5sum
            full_path = output_path.joindir(fastq_file_name)
            process = subprocess.Popen(['md5sum', full_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

            stdout, _ = process.communicate()

            if stdout.decode('UTF-8').split(' ')[0] != fastq_md5checksum:
                return False
            print(f'Checksum OK')

            # Rename the file
            full_path.rename(output_path.join(file_name))

    return True


def download_file(input_csv_path, base_path, ssh_key_path):
    input_df = pd.read_csv(input_csv_path)

    # Add metadata column
    if 'finished' not in input_df:
        input_df['finished'] = np.nan

    # Go trough every line of the file
    for index, row in input_df.iterrows():

        print('=========== Parse file ============')
        print(row)
        print()

        # Skip if this file has been downloaded
        if pd.notna(row['finished']):
            print('Already downloaded, skip\n')
            continue

        # Parse row details
        geo_id = row['GEO #']
        file_id = row['file #']
        file_name = row['file_name']

        # Create output paths
        output_path = base_path.joinpath(geo_id, file_id)
        output_path.mkdir(exist_ok=True, parents=True)

        # Get run details from GEO ID
        srx_id_list = geo_id_to_srx_ids(file_id)
        print(f'{file_id} is associated with the following ID(s): {srx_id_list}')

        for srx_id in srx_id_list:

            # Download file, if unsuccessful add tag
            print(f'Start downloading file for SRA ID {srx_id}')
            if download_run(srx_id, output_path=output_path, file_name=file_name, ssh_key_path=ssh_key_path):
                input_df.loc[index, 'finished'] = True
            else:
                print("Download file failed")
                continue

        input_df.to_csv(input_csv_path.with_suffix('.tmp'))
        print('Done')


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description='Download fastq files from a given list of GEO IDs')
    parser.add_argument('--input', type=str, required=True, help="Path to the input csv file")
    parser.add_argument('--output', type=str, required=True, help="Path to write the downloaded samples to")
    parser.add_argument('--resume', action="store_true", help="If specified resume downloading")
    parser.add_argument('--ssh-key-file', type=str,
                        default=Path('~/.aspera/cli/etc/asperaweb_id_dsa.openssh').expanduser(),
                        help="Path to the ssh key file used by the aspera client")

    args = parser.parse_args()

    # Config options
    input_csv_path = Path(args.input)
    output_path = Path(args.output)
    ssh_key_path = Path(args.ssh_key_file)

    # If resume specified, check if resume file (ends with '.tmp') exists
    if args.resume:
        resume_file_path = output_path.with_suffix(".tmp")
        if resume_file_path.is_file():
            input_csv_path = resume_file_path

    # Start downloading
    download_file(input_csv_path, output_path, ssh_key_path)
