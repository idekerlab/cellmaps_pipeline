#! /usr/bin/env python


import sys
import pandas as pd

if len(sys.argv) != 3:
    msg = """
    Usage <samples.csv or unique.csv from HPA> <file with ensembl_ids>
    
    Filters samples or unique csv files, keeping only rows with ensembl_ids
    in 'ensembl_ids' column found in 2nd file passed in. 
    
    NOTE: 2nd file must have a header line 'ensembl_ids' and samples.csv|unique.csv
    file must have ensembl_ids column. If that column has commas in it, this
    tool may skip those entries. 
    """
    sys.stderr.write(msg + '\n\n')
    sys.stderr.flush()
    sys.exit(1)

df = pd.read_csv(sys.argv[1])

ensembl_df = pd.read_csv(sys.argv[2])
ensembl_ids = set(ensembl_df['ensembl_ids'].values)

filtered_df = df[df['ensembl_ids'].isin(ensembl_ids)]


filtered_df.to_csv(sys.argv[1] + '_filtered.csv', index=False)