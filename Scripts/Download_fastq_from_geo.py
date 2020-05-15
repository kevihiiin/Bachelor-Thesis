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
ncbi_database = 'gds'
esearch_path = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={}&term={}'
efetch_path = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={}&id={}'

ssh_key_file = '$HOME/.aspera/cli/etc/asperaweb_id_dsa.openssh'


def id_to_efetch_ids(supplied_id, database='gds'):
    """
    Get IDs for efetch from an accession ID (e.g GEO)
    :param supplied_id: Accession ID (e.g GEO) to get more infos from
    :param database: Database the accession ID is from (e.g 'gds')
    :return: list of associated IDs for efetch
    """
    result = requests.get(esearch_path.format(database, supplied_id))

    # If request was unsuccessful stop
    if result.status_code != 200:
        raise RuntimeError

    # Parse as XML
    result_tree = etree.fromstring(result.content)

    # Stop if the parent / root attribute is not eSearchResults
    if result_tree.tag != 'eSearchResult':
        raise RuntimeError(result_tree.attrib)

    # Return empty list directly if there were no results
    id_count = 0
    id_list = []

    for child in result_tree.getchildren():
        child_tag = child.tag
        if child_tag == 'Count':
            id_count = int(child.text)
        elif child_tag == 'IdList':
            id_list = [x.text for x in child.getchildren()]

    assert len(id_list) == id_count

    return id_list


def efetch_ids_to_text_and_srx_list(efetch_id_list, database='gds'):
    """
    Get text for the efetch IDs and extract SRA experiemnt accession IDs (SRX IDs)
    :param database: Database the accession ID is from (e.g 'gds')
    :param efetch_id_list: list with IDs to fetch information from
    :return: concatenated text from all IDs ; list of SRX IDs
    """

    # The text from all the sites
    id_text = ''

    # Fetch the text for all the IDs
    for efetch_id in efetch_id_list:
        result = requests.get(efetch_path.format(database, efetch_id))
        if result.status_code != 200:
            raise RuntimeError

        # Fetch the text
        result_text = result.content.decode('UTF-8')
        # Add the text to the result text
        id_text += result_text

    # Extract the SRX IDs from the text
    srx_id_list = re.findall(r'SRA Run Selector: .*?=(SRX.*)', id_text)

    return id_text, srx_id_list


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

        cmd = "ascp -QT -l 300m -P33001 {} -i {} {} {}".format(
            "",  # Additional args
            ssh_key_file,
            fastq_aspera_path,
            full_path)
        subprocess.check_call(cmd, shell=True)

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
    for _, row in input_df.iterrows():

        # Skip if this file has been downloaded
        if row['finished']:
            continue

        # Parse row details
        geo_id = row['GEO #']
        file_id = row['file #']
        file_name = row['file name']

        # Create output paths
        output_path = os.path.join(base_path, geo_id, geo_id)
        file_name = f'{file_id}.fastq.gz'

        # Get run details from GEO ID
        run_text, srx_id_list = efetch_ids_to_text_and_srx_list(id_to_efetch_ids(geo_id))

        # Write run information to file:
        with open(os.path.join(output_path, f'{file_name}.txt'), 'w') as file:
            file.writelines(run_text)

        # Download file, if unsuccessful add tag
        if download_run(srx_id_list, output_directory=output_path, file_name=file_name):
            input_df['finished'] = True


if __name__ == '__main__':
    # id_list = id_to_efetch_ids(geo_id)
    # print(id_list)
    # id_text, srx_list = efetch_ids_to_text_and_srx_list(id_list)
    # print(id_text, srx_list)
    # download_run('SRX4169538', '/home/')
    download_file('/home/kevin/dummy.csv')
