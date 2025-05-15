===========================
Usage via command line
===========================


The pipeline provides a command line tool ``cellmaps_pipelinecmd.py`` that can run
the pipeline serially or in parallel via `SLURM`_ For more information run the following:

The example below runs the pipeline using example data. This may take up to an hour to run.


.. code-block:: python

    cellmaps_pipelinecmd.py myexample_run --samples examples/samples.csv \
                            --unique examples/unique.csv \
                            --edgelist examples/edgelist.tsv \
                            --baitlist examples/baitlist.tsv \
                            --provenance examples/provenance.json \
                            --ppi_cutoffs 0.01 0.1

.. note::

   Above assumes the `repo <https://github.com/idekerlab/cellmaps_pipeline>`__ has been cloned
   locally and the command above is run within the base directory of the repo


.. _CM4AI data: https://cm4ai.org/data
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
.. _SLURM: https://slurm.schedmd.com/documentation.html
