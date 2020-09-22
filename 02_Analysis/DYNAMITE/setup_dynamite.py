#!/usr/bin/env python

import argparse
import csv
from jinja2 import Template
from pathlib import Path

# Argument parser
parser = argparse.ArgumentParser(description='DYNAMITE Setup generator')
parser.add_argument('--dynamite', type=str, required=True, help="Dynamite path")
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--config', default='setup_file_all.tsv', type=str)
parser.add_argument('--template', default='DYNAMITE-TEMPLATE.cfg', type=str)

args = parser.parse_args()

# Config options
config_file = args.config
config_template_file = args.template
output_base_path = Path(args.output)
dynamite_path = Path(args.dynamite)


# Load settings template
with open(config_template_file) as file_:
    config_template = Template(file_.read())

# Load and process setup file
with open(config_file) as csv_file:
    dict_reader = csv.DictReader(csv_file, delimiter='\t')

    # For each sample setup folder
    for sample in dict_reader:
        time_point = sample['time']
        hm = sample['hm']

        # --- Create folder structure
        output_path = output_base_path.joinpath('DYNAMITE', time_point, hm)
        output_path.mkdir(parents=True, exist_ok=True)

        # --- Create DYNAMITE configuration file
        # Differential gene expression file
        deg_file = output_base_path.joinpath('DESeq2', time_point, f'{time_point}-deseq_dynamite.tsv')
        # TEPIC output
        time_group1, _, time_group2 = time_point.split('_')
        tepic_group1 = output_base_path.joinpath('TEPIC', time_group1, hm)
        tepic_group2 = output_base_path.joinpath('TEPIC', time_group2, hm)
        # Populate template
        context = {
            'out_dir': output_path,
            'deg_file': deg_file,
            'tepic_group1': tepic_group1,
            'tepic_group2': tepic_group2,
            'dynamite_path': dynamite_path.joinpath('Scripts'),
        }

        with open(output_path.joinpath('DYNAMITE.cfg'), 'w') as dynamite_config_file:
            dynamite_config_file.write(config_template.render(context))
