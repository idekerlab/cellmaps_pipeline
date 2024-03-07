=====
Usage
=====

This page should provide information on how to use cellmaps_pipeline

In a project
--------------

To use Cell Maps Pipeline in a project:

.. code-block:: python

    import os
    import json
    from cellmaps_pipeline.runner import ProgrammaticPipelineRunner
    from cellmaps_pipeline.runner import CellmapsPipeline

    # load the provenance as a dict
        with open(os.path.join('examples', 'provenance.json'), 'r') as f:
            json_prov = json.load(f)

    runner = ProgrammaticPipelineRunner(outdir='testrun',
                                        samples=os.path.join('examples', 'samples.csv'),
                                        unique=os.path.join('examples', 'unique.csv'),
                                        edgelist=os.path.join('examples', 'edgelist.tsv'),
                                        baitlist=os.path.join('examples', 'baitlist.tsv'),
                                        model_path='https://github.com/CellProfiling/densenet/releases/download/v0.1.0/external_crop512_focal_slov_hardlog_class_densenet121_dropout_i768_aug2_5folds_fold0_final.pth',
                                        provenance=json_prov,
                                        ppi_cutoffs=[0.001, 0.01],
                                        input_data_dict={})

    pipeline = CellmapsPipeline(outdir='testrun',
                                runner=runner,
                                input_data_dict={})
    print('Status code: ' + str(pipeline.run()))


Example usage for CM4AI data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The cell maps pipeline requires two `RO-Crate`_ directories from `CM4AI data`_ site

Visit https://cm4ai.org/data, login and accept agreement


For ImmunoFluorescent images `RO-Crate`_

1) If not already there navigate to **Data** tab:

   .. image:: images/datatab.png
      :alt: Screenshot of data, cell maps, and intermediate other tabs with data selected

2) On left side bar under **Name** check ``IF images`` checkbox, check ``MDA-MB-468``
   for **Cell Line**, ``untreated`` for **Treatment**, ``chromatin`` for **Gene Set**,
   and ``0.1 alpha`` for **Version**:

   .. image:: images/if_leftsidebar.png
      :alt: Screenshot of left side bar showing IF images, MDA-MB-468, untreated, chromatin, and 0.1 alpha boxes checked

3) Click **Download** link on row:

   .. image:: images/if_download.png
      :alt: Screenshot of browser showing row of ImmunoFluorescent image dataset to download

For AP-MS `RO-Crate`_

1) If not already there navigate to **Data** tab
2) On left side bar under **Name** check ``AP-MS`` checkbox, check ``MDA-MB-468``
   for **Cell Line**, ``untreated`` for **Treatment**, ``chromatin`` for **Gene Set**,
   and ``0.1 alpha`` for **Version**
3) Click **Download** link on row


Example usage using data from `Human Protein Atlas`_ and `Bioplex`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

.. _CM4AI data: https://cm4ai.org/data
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
