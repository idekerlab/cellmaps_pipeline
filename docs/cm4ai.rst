=============================
Example usage for CM4AI data
=============================

The cell maps pipeline requires two `RO-Crate`_ directories from `CM4AI data`_ site


Step 1) Get data from `CM4AI`_ site
-------------------------------------

Visit https://cm4ai.org/data, login and accept agreement


For ImmunoFluorescent images `RO-Crate`_

1) If not already set, navigate to **Data** tab:

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

1) If not already set, navigate to **Data** tab

   .. image:: images/datatab.png
      :alt: Screenshot of data, cell maps, and intermediate other tabs with data selected

2) On left side bar under **Name** check ``AP-MS`` checkbox, check ``MDA-MB-468``
   for **Cell Line**, ``untreated`` for **Treatment**, ``chromatin`` for **Gene Set**,
   and ``0.1 alpha`` for **Version**

   .. image:: images/apms_leftsidebar.png
      :alt: Screenshot of left side bar showing AP-MS, MDA-MB-468, untreated, chromatin, and 0.1 alpha boxes checked


3) Click **Download** link on row

   .. image:: images/apms_download.png
      :alt: Screenshot of browser showing row of AP-MS dataset to download


Step 2) Uncompress downloaded data from `CM4AI`_ site
-------------------------------------------------------

The above steps will download two files:

* ``cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha.tar.gz`` containing the AP-MS dataset
* ``cm4ai_chromatin_mda-mb-468_untreated_ifimage_0.1_alpha.tar.gz`` containing ImmunoFluorescent image dataset

These files need to be `untarred`_ and gunzipped to be used by the `cellmaps_pipeline`_


Easiest way to do this on Linux/Mac is to open and terminal and run the following:

.. code-block:: python

    tar -zxf cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha.tar.gz
    tar -zxf cm4ai_chromatin_mda-mb-468_untreated_ifimage_0.1_alpha.tar.gz

.. note::

    Before running above command be sure to change to directory where those files reside


Step 3) Run the `cellmaps_pipeline`_ on `CM4AI`_ data
---------------------------------------------------------

.. code-block:: python

    cellmaps_pipelinecmd.py . --example_provenance > pipe_prov.json
    # be sure to update pipe_prov.json file

    cellmaps_pipelinecmd.py  --provenance pipe_prov.json \
                            --cm4ai_apms cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha/apms.tsv \
                            --cm4ai_image cm4ai_chromatin_mda-mb-468_untreated_ifimage_0.1_alpha/MDA-MB-468_untreated_antibody_gene_table.tsv

.. note::

    Above command may fail to run on machines with 16gb of ram or less


.. _CM4AI data: https://cm4ai.org/data
.. _CM4AI: https://cm4ai.org
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
.. _untarred: https://en.wikipedia.org/wiki/Tar_(computing)
.. _gunzipped: https://en.wikipedia.org/wiki/Gzip#File_format
