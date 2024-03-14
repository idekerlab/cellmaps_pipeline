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

Each tool of the pipeline can be run separately in the following way:

.. code-block::

    # Download ImmunoFluorescent image data
    cellmaps_imagedownloadercmd.py ./cellmaps_imagedownloader_outdir  --samples examples/samples.csv \
                                   --unique examples/unique.csv --provenance examples/provenance.json

    # Download Affinity-Purification mass spectrometry (AP-MS) data as a Protein-Protein Interaction network
    cellmaps_ppidownloadercmd.py ./cellmaps_ppidownloader_outdir --edgelist examples/edgelist.tsv \
                                 --baitlist examples/baitlist.tsv --provenance examples/provenance.json

    # Generate embeddings from ImmunoFluorescent image data
    cellmaps_image_embeddingcmd.py ./cellmaps_image_embedding_outdir --inputdir ./cellmaps_imagedownloader_outdir
                                   --fold 1

    # Generate embeddings from Protein-Protein interaction networks using node2vec
    cellmaps_ppi_embeddingcmd.py ./cellmaps_ppi_embedding_outdir --inputdir ./cellmaps_ppidownloader_outdir

    # Generate co-embedding from image and Protein-Protein Interaction (PPI) embeddings
    cellmaps_coembeddingcmd.py ./cellmaps_coembedding_outdir --image_embeddingdir ./cellmaps_image_embedding_outdir \
                               --ppi_embeddingdir ./cellmaps_ppi_embedding_outdir

    # Generate hierarchy from coembeddings using HiDeF.
    cellmaps_generate_hierarchycmd.py ./cellmaps_generate_hierarchy_outdir --coembedding_dirs ./cellmaps_coembedding_outdir

    # Annotate a hierarchy by performing enrichment against three NDEx networks HPA, CORUM, and GO-CC
    cellmaps_hierarchyevalcmd.py ./cellmaps_hierarchyeval_outdir --hierarchy_dir ./cellmaps_generate_hierarchy_outdir

To run the pipeline programmatically, follow the steps detailed in the following notebook: `A Step-By-Step Guide to Building Cellmaps Pipeline`_

.. _A Step-By-Step Guide to Building Cellmaps Pipeline: https://github.com/idekerlab/cellmaps_pipeline/blob/main/notebooks/step-by-step-guide-run-cellmaps-pipeline.ipynb
.. _CM4AI data: https://cm4ai.org/data
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
