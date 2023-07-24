=====
Usage
=====

This page should provide information on how to use cellmaps_pipeline

In a project
--------------

To use CM4AI Pipeline in a project::

    import cellmaps_pipeline

On the command line
---------------------

For information invoke :code:`cellmaps_pipelinecmd.py -h`

**Example usage**

**TODO:** Add information about example usage

.. code-block::

   # use wget to download model or directly visit url below to download the model file
   # to current directory
   wget https://github.com/CellProfiling/hpa_densenet/raw/main/models/bestfitting_default_model.pth

   cellmaps_pipelinecmd.py toyrun --samples examples/samples.csv --unique examples/unique.csv \
                           --baitlist examples/baitlist.tsv --edgelist examples/edgelist.tsv \
                           --provenance examples/provenance.json --model_path bestfitting_default_model.pth
