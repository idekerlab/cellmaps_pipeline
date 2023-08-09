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

**Example usage**

The cell maps pipeline requires five input files for building MuSIC maps by integrating IF images with an AP-MS interaction network: 

1) samples file: information on image links for download (see sample samples file in examples folder)
2) unique file: information on antibody to use for each gene (see sample unique file in examples folder)
3) bait list file: list of baits used for AP-MS experiments
4) edge list file: list of edges for AP-MS interaction network
5) image embedding model: see below for how to download

.. code-block::

   # use wget to download model or directly visit url below to download the model file
   # to current directory
   wget https://github.com/CellProfiling/hpa_densenet/raw/main/models/bestfitting_default_model.pth

   cellmaps_pipelinecmd.py toyrun --samples examples/samples.csv --unique examples/unique.csv \
                           --baitlist examples/baitlist.tsv --edgelist examples/edgelist.tsv \
                           --provenance examples/provenance.json --model_path bestfitting_default_model.pth
