#! /usr/bin/env python

import sys
import pandas as pd
import mygene

if len(sys.argv) != 3:
    msg = """
    Usage <ppi_scoring.txt> <dest file prefix>

    Converts ppi_scoring.txt file to bioplex format.
    THIS ASSUMES THE BAIT is PIK3CA and updates the values
    accordingly!!!!
    
    """
    sys.stderr.write(msg + '\n\n')
    sys.stderr.flush()
    sys.exit(1)

df = pd.read_csv(sys.argv[1], delimiter='\t')

# remove entries where BFDR.x is greater then 0.05
filtered_df = df[df['BFDR.x'] < 0.05]

# grab only the two columns we need
bait_prey_df = filtered_df[['Bait', 'Prey']]

# check baits are H
baits = set(bait_prey_df['Bait'].values)

for b in baits:
    if 'HSC2' not in b:
        sys.stderr.write('Expected bait to contain HSC2\n'
                         'because it is assumed they are all PIK3CA\n'
                         'Exiting\n\n')
        sys.stderr.flush()
        sys.exit(1)

# Add new entrez id column by querying mygene
mg = mygene.MyGeneInfo()

# the Prey values are uniprot ids
uniprotids = list(df['Prey'].values)

# query mygene for the symbol
res = mg.querymany(uniprotids, species='human',
                   scopes='uniprot',
                   fields=['symbol', 'ensembl.gene'])

edgelist = {'GeneID1': [],
            'Symbol1': [],
            'GeneID2': [],
            'Symbol2': []}

ensembl_ids = set()

for entry in res:
    if 'symbol' not in entry:
        continue
    if 'ensembl' in entry:
        print(entry)
        if isinstance(entry['ensembl'], dict):
            ensembl_ids.add(entry['ensembl']['gene'])
        else:
            for ensem in entry['ensembl']:
                ensembl_ids.add(ensem['gene'])

    edgelist['GeneID1'].append('101928739')
    edgelist['Symbol1'].append('PIK3CA')
    edgelist['GeneID2'].append(entry['_id'])
    edgelist['Symbol2'].append(entry['symbol'])


df = pd.DataFrame(edgelist,
                  columns=['GeneID1', 'Symbol1', 'GeneID2', 'Symbol2'])

df.to_csv(sys.argv[2] + '_edgelist.tsv', sep='\t', index=False)

df = pd.DataFrame({'GeneSymbol': ['PIK3CA'],
                   'GeneID': ['101928739'],
                   '# Interactors': len(df)})

df.to_csv(sys.argv[2] + '_baitlist.tsv', sep='\t', index=False)

df = pd.DataFrame({'ensembl_ids': list(ensembl_ids)},
                  columns=['ensembl_ids'])
df.to_csv(sys.argv[2] + '_ensembl_ids.tsv', sep='\t', index=False)
