#! /usr/bin/env python

import os
import sys
import pandas as pd


if len(sys.argv) != 3:
    sys.stderr.write('Usage: <listOfFiles.csv> <outdir>')
    sys.stderr.write('\nThis script takes listOfFiles.csv '
                     'and converts it to samples.csv,unique.csv'
                     ', and proteinatlas.xml files compatible '
                     'with cellmaps_imagedownloader')
    sys.stderr.flush()
    sys.exit(1)

df = pd.read_csv(sys.argv[1])
print()
print(df.head())
print('# rows: ' + str(len(df)))
print('\nKeeping only slice z01')
z01_df = df[df['Slice'] == 'z01']
print(z01_df.head())
print('# rows: ' + str(len(z01_df)))

print('\nRemoving rows where gene is None')
z01_valid_df = z01_df[z01_df['Antibody'] != 'NEGATIVE-CTRL']

print(z01_valid_df.head())
print('# rows: ' + str(len(z01_valid_df)))

print('\nRename columns')
renamed_df = z01_valid_df.copy()
renamed_df.rename(columns={'Antibody': 'antibody',
                           'Region': 'position',
                           'Slice': 'sample',
                           'RegionID': 'filename',
                           'Treatment': 'if_plate_id',
                           'Gene': 'gene_names'}, inplace=True)
print(renamed_df.head())

print('\nPrefix if_plate_id')
renamed_df['if_plate_id'] = 'B2AI_1_' + renamed_df['if_plate_id'].astype(str)
print(renamed_df.head())

sys.exit(0)

outdir = sys.argv[2]

if not os.path.isdir():
    os.makedirs(sys.argv[2], mode=0o755)

