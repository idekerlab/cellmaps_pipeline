#! /usr/bin/env python

import os
import sys
import pandas as pd
import mygene


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
                           'Gene': 'gene_names',
                           'Baselink': 'linkprefix'}, inplace=True)
print(renamed_df.head())

print('\nPrefix if_plate_id and add slice to filename')
renamed_df['if_plate_id'] = 'B2AI_1_' + renamed_df['if_plate_id'].astype(str) +\
                            '_' + renamed_df['Well'].astype(str)
renamed_df['filename'] = renamed_df['filename'].astype(str) +\
                         '_' + renamed_df['sample'].astype(str) + '_'
renamed_df.drop('Well', axis=1, inplace=True)

print(renamed_df.head())

print('\nAdd locations and ensembl_ids columns')
renamed_df['locations'] = ''
renamed_df['ensembl_ids'] = ''

print('\nReorder columns and replace _ with comma in gene_names')

final_sample_df = renamed_df[['filename', 'if_plate_id', 'position',
                              'sample', 'locations', 'antibody', 'ensembl_ids',
                              'gene_names', 'linkprefix']]
final_sample_df['gene_names'] = final_sample_df['gene_names'].str.replace('_', ',')
print(final_sample_df.head())


print('\nQuery mygene to get ensemble ids')

gene_names_list = final_sample_df['gene_names'].values.tolist()
gene_name_set = set(gene_names_list)
print(gene_name_set)
new_genes_to_add = set()
entries_to_remove = set()
for entry in gene_name_set:
    if ',' in entry:
        new_genes_to_add.update(entry.split(','))

gene_name_set.update(new_genes_to_add)

for entry in entries_to_remove:
    gene_name_set.remove(entry)

# get ensembl ids
mygeneinfo=mygene.MyGeneInfo()

res = mygeneinfo.querymany(list(gene_name_set),
                           scopes=['symbol', 'HGNC'],
                           fields=['ensembl.gene'],
                           species='human')


res_dict = {}
for entry in res:
    if 'notfound' in entry:
        continue
    ensembl_ids = []
    if isinstance(entry['ensembl'], list):
        for subentry in entry['ensembl']:
            ensembl_ids.append(subentry['gene'])
    else:
        ensembl_ids.append(entry['ensembl']['gene'])

    res_dict[entry['query']] = ensembl_ids

# print(res_dict)

gene_ensembl_dict = {}
for gene in gene_names_list:
    ensembl_ids = set()
    if ',' in gene:
        for g in gene.split(','):
            if g in res_dict:
                ensembl_ids.update(res_dict[g])
    else:
        if gene in res_dict:
            ensembl_ids.update(res_dict[gene])
    gene_ensembl_dict[gene] = ','.join(ensembl_ids)

print(gene_ensembl_dict)

for key in gene_ensembl_dict:
    final_sample_df.loc[final_sample_df['gene_names'] == key, 'ensembl_ids'] = gene_ensembl_dict[key]

print(final_sample_df.head())


outdir = sys.argv[2]

if not os.path.isdir(outdir):
    os.makedirs(sys.argv[2], mode=0o755)

for treatment in ['Paclitaxel', 'untreated', 'Vorinostat']:
    temp_df = final_sample_df[final_sample_df['filename'].str.contains(treatment)]
    temp_df.to_csv(os.path.join(outdir, 'samples_' + treatment.lower() + '.csv'), index=False)
    # need to make unique.csv now
    temp_unique_df = temp_df.groupby('antibody').head(1).reset_index(drop=True)
    temp_unique_df.drop(['filename', 'position', 'sample', 'if_plate_id',
                         'linkprefix'], axis=1, inplace=True)
    temp_unique_df['n_location'] = 0
    temp_unique_df['atlas_name'] = 'MDA-MB-469'
    unique_df =temp_unique_df[['antibody', 'ensembl_ids', 'gene_names',
                               'atlas_name', 'locations', 'n_location']]
    print(unique_df.head())
    unique_df.to_csv(os.path.join(outdir, 'unique_' + treatment.lower() + '.csv'), index=False)


