=============================
Example usage for CM4AI data
=============================

The cell maps pipeline requires two `RO-Crate`_ directories from `CM4AI data`_ site


Step 1) Get data from `CM4AI`_ site
-------------------------------------

Visit https://cm4ai.org/data-releases/, and pick ``CM4AI 0.5 Alpha Data Release`` release. You will be redirected
to `UVA Dataverse` web page.

    .. image:: images/cm4aireleaseweb.png
      :alt: Data release site on CM4AI web page

For ImmunoFluorescent images `RO-Crate`_

1) Click on the Files tab, and use regex expression to search for ``*ifimage*``. List of data bundles with IF images
will be displayed. Check the name of the bundle to identify the treatment, cell line, and any other relevant
information. For this example with download images for ``paclitaxel`` treatment.

   .. image:: images/searchifimage.png
      :alt: IF images files in dataverse

2) Click the ``Download button`` on the right-hand side of the file bundle you want to download and choose
``Zip Archive``.

   .. image:: images/downloadzip.png
      :scale: 50%
      :alt: Download zip file

3) Accept data release agreement. The zip file will be downloaded.

   .. image:: images/acceptagreement.png
      :alt: Data release agreement dialog

For AP-MS `RO-Crate`_

1) For AP-MS data the steps are the same. Click on the Files tab, and use regex expression to search for ``*apms*``. Click the ``Download button`` on the right-hand side of the file bundle you want to download and choose
``Zip Archive``. Accept data release agreement. The zip file will be downloaded.

   .. image:: images/apmsdownload.png
      :alt: AP-MS file in dataverse


Step 2) Uncompress downloaded data from `CM4AI`_ site
-------------------------------------------------------

The above steps will download two files:

* ``cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha.zip`` containing the AP-MS dataset
* ``cm4ai_chromatin_mda-mb-468_paclitaxel_ifimage_0.1_alpha.zip`` containing ImmunoFluorescent image dataset

These files need to be `unzipped`_ to be used by the `cellmaps_pipeline`_


Easiest way to do this on Linux/Mac is to open and terminal and run the following:

.. code-block:: bash

    unzip cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha.zip
    unzip cm4ai_chromatin_mda-mb-468_paclitaxel_ifimage_0.1_alpha.zip

.. note::

    Before running above command be sure to change to directory where those files reside


Step 3) Run the `cellmaps_pipeline`_ on `CM4AI`_ data
---------------------------------------------------------

.. code-block:: python

    cellmaps_pipelinecmd.py . --example_provenance > pipe_prov.json
    # be sure to update pipe_prov.json file

    cellmaps_pipelinecmd.py ./output_dir --provenance pipe_prov.json --cm4ai_apms cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha/apms.tsv --cm4ai_image cm4ai_chromatin_mda-mb-468_paclitaxel_ifimage_0.1_alpha/MDA-MB-468_paclitaxel_antibody_gene_table.tsv

.. note::

    Above command may fail to run on machines with 16gb of ram or less


.. _CM4AI data: https://cm4ai.org/data
.. _CM4AI: https://cm4ai.org
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
.. _unzipped: https://en.wikipedia.org/wiki/ZIP_(file_format)
