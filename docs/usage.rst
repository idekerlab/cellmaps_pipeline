=====
Usage
=====

This page provides information on how to use `cellmaps_pipeline`_


Usage via command line
-----------------------

The pipeline provides a command line tool ``cellmaps_pipelinecmd.py`` that can run
the pipeline serially or in parallel via `SLURM`_ For more information run the following:

.. code-block:: python

    cellmaps_pipelinecmd.py -h

Usage programmatically
-----------------------

The pipeline can be invoked programmatically to run all the steps in the pipeline
serially via the :py:class:`~cellmaps_pipeline.runner.ProgrammaticPipelineRunner` as seen
in the example below,
or via `SLURM`_ using :py:class:`~cellmaps_pipeline.runner.SLURMPipelineRunner`


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


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   provenance
   cm4ai
   hpa_bioplex
   ndex_save


.. _CM4AI data: https://cm4ai.org/data
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
.. _SLURM: https://slurm.schedmd.com/documentation.html
