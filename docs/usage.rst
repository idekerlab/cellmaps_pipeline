=====
Usage
=====

This page should provide information on how to use cellmaps_pipeline

In a project
--------------

To use Cell Maps Pipeline in a project::

    import cellmaps_pipeline

On the command line
---------------------

For information invoke :code:`cellmaps_pipelinecmd.py -h`

**Example usage for CM4AI data**

Coming soon...

**Example usage**

The cell maps pipeline requires the following input files for building MuSIC maps by integrating IF images with an AP-MS interaction network: 

1) samples file: CSV file with list of IF images to download (see sample samples file in examples folder)
2) unique file: CSV file of unique samples (see sample unique file in examples folder)
3) bait list file: TSV file of baits used for AP-MS experiments
4) edge list file: TSV file of edges for protein interaction network
5) provenance: file containing provenance information about input files in JSON format (see sample provenance file in examples folder)

.. code-block::

   cellmaps_pipelinecmd.py ./cellmaps_pipeline_outdir --samples examples/samples.csv --unique examples/unique.csv \
                           --baitlist examples/baitlist.tsv --edgelist examples/edgelist.tsv \
                           --provenance examples/provenance.json
