#! /usr/bin/env python3
import os
import re
import subprocess
import requests
import pandas as pd
import numpy as np

from lxml import etree

# Inspired by
# https://github.com/wwood/ena-fast-download/blob/master/ena-fast-download.py

# --- Constants ---
accession_path = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={}&targ=self&form=text&view=brief'

ssh_key_file = os.path.expanduser('~/.aspera/cli/etc/asperaweb_id_dsa.openssh')


def geo_id_to_srx_ids(geo_id):
    result = requests.get(accession_path.format(geo_id))

    # If request was unsuccessful stop
    if result.status_code != 200:
        raise RuntimeError

    id_text = result.content.decode('UTF-8')

    srx_id_list = [x.strip() for x in re.findall(r'!Sample_relation = SRA: .*?=(SRX.*)', id_text)]

    return srx_id_list


def download_run(run_id, output_directory, file_name=None):
    result_json = requests.get(
        f'https://www.ebi.ac.uk/ena/portal/api/filereport?accession={run_id}&download=false&fields=fastq_aspera%2Cfastq_md5&format=json&result=read_run').json()

    # No specific filename if there is more than one file to download
    if len(result_json) > 1:
        file_name = None

    for single_run in result_json:
        fastq_aspera_path = single_run['fastq_aspera']
        fastq_md5checksum = single_run['fastq_md5']

        if not file_name:
            file_name = os.path.basename(fastq_aspera_path)

        full_path = os.path.join(output_directory, file_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        cmd = "ascp -QT -l 500m -P33001 {} -i {} era-fasp@{} {}".format(
            "",  # Additional args
            ssh_key_file,
            fastq_aspera_path,
            full_path)
        process = subprocess.check_call(cmd, stdout=subprocess.PIPE, shell=True)

        print(f'Retval: {process}')

        # Check md5sum
        process = subprocess.Popen(['md5sum', full_path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, _ = process.communicate()

        if stdout.decode('UTF-8').split(' ')[0] != fastq_md5checksum:
            return False


def download_file(input_csv, base_path=''):
    input_df = pd.read_csv(input_csv)

    # Add metadata column
    if 'finished' not in input_df:
        input_df['finished'] = np.nan

    # Go trough every line of the file
    for index, row in input_df.iterrows():

        print('=== Parse file ===')
        print(row)

        # Skip if this file has been downloaded
        if pd.notna(row['finished']):
            print('Already downloaded, skip')
            continue

        # Parse row details
        geo_id = row['GEO #']
        file_id = row['file #']
        file_name = row['file name']

        # Create output paths
        output_path = os.path.join(base_path, geo_id, file_id)
        file_name = f'{file_name}.fastq.gz'

        # Get run details from GEO ID
        srx_id = geo_id_to_srx_ids(file_id)[0]
        print(f'{file_id} is associated with the following ID(s): {srx_id}')

        # # Write run information to file:
        # with open(os.path.join(output_path, f'{file_name}.txt'), 'w') as file:
        #     file.writelines(run_text)

        # Download file, if unsuccessful add tag
        print(f'Start downloading files...')
        valid_file = download_run(srx_id, output_directory=output_path, file_name=file_name)

        if valid_file:
            input_df.loc[index, 'finished'] = True

        input_df.to_csv(input_csv + '.out')

        print('Done')


if __name__ == '__main__':
    download_file('GEO data list.csv', '/localscratch/kyuan')

