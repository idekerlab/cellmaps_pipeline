=====================================================================
Example usage using data from `Human Protein Atlas`_ and `Bioplex`_
=====================================================================

The cell maps pipeline requires the following input files for building MuSIC maps by integrating IF images with an AP-MS interaction network:

1) samples file: CSV file with list of IF images to download (see sample samples file in examples folder)
2) unique file: CSV file of unique samples (see sample unique file in examples folder)
3) bait list file: TSV file of baits used for AP-MS experiments
4) edge list file: TSV file of edges for protein interaction network
5) provenance: file containing provenance information about input files in `JSON`_ format
   (see sample provenance file in examples folder, or create one directly as described above)

.. code-block::

   cellmaps_pipelinecmd.py ./cellmaps_pipeline_outdir --samples examples/samples.csv --unique examples/unique.csv \
                           --baitlist examples/baitlist.tsv --edgelist examples/edgelist.tsv \
                           --provenance examples/provenance.json

.. _CM4AI data: https://cm4ai.org/data
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
