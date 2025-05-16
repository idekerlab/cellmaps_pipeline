=============================
Example usage for CM4AI data
=============================

Example usage using CM4AI 0.5 Alpha Data Release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Visit `cm4ai.org <https://cm4ai.org>`__ and go to **Products -> Data Releases**

#. Scroll down and click **CM4AI 0.5 Alpha Data Release** link (circled in red)

    .. image:: images/datarelease_0.5link.png
        :alt: Link to CM4AI 0.5 data release circled in red

#. On the newly opened page/tab, scroll down to the **cm4ai_chromatin_mda-mb-468_paclitaxel_ifimage_0.1_alpha** entry
   and click the download icon (circled in red) to bring up a pop up dialog. Click **Zip Archive** (red arrow)
   to accept the usage agreement and download the dataset

    .. image:: images/0.5imagedownload_paclitaxel.png
        :alt: CM4AI 0.5 paclitaxel image zip download link circled in red

    .. note::

        For **vorinostat** dataset, look for **cm4ai_chromatin_mda-mb-468_vorinostat_ifimage_0.1_alpha.zip** entry and perform the same
        operations above.

    .. note::

        For **untreated** dataset, click `here <https://g-9b3b6e.9ad93.a567.data.globus.org/Data/cm4ai_0.1alpha/cm4ai_chromatin_mda-mb-468_untreated_ifimage_0.1_alpha.tar.gz>`__ to download the images
        which are stored as a tarred gzip file

#. Do the same as above to download the **cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha** entry

#. Unzip files

    This can be done by double clicking on the file or if on a Mac/Linux machine by running the following
    on a command line:

    .. code-block::

        unzip cm4ai_chromatin_mda-mb-468_paclitaxel_ifimage_0.1_alpha.zip
        unzip cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha.zip


#. Running cellmaps_pipelinecmd command

    .. code-block::

       # Be sure to unzip the zip files above before running this step

       cellmaps_pipelinecmd.py . --example_provenance > pipe_prov.json

       # Be sure to update pipe_prov.json file

       cellmaps_pipelinecmd.py ./paclitaxel_run --provenance pipe_prov.json \
             --cm4ai_apms cm4ai_chromatin_mda-mb-468_untreated_apms_0.1_alpha/apms.tsv \
             --cm4ai_image cm4ai_chromatin_mda-mb-468_paclitaxel_ifimage_0.1_alpha/MDA-MB-468_paclitaxel_antibody_gene_table.tsv

    .. note::

    Above command may fail to run on machines with 16gb of ram or less

Example usage February 2025 Data Release (Beta)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Visit `cm4ai.org <https://cm4ai.org>`__ and go to **Products -> Data Releases**

#. Scroll down and click **February 2025 Data Release (Beta)** link (circled in red)

    .. image:: images/datarelease_0.6link.png
        :alt: Link to CM4AI February 2025 data release circled in red

#. On the newly opened page/tab, scroll down to the **cm4ai-v0.6-beta-if-images-paclitaxel.zip** entry
   and click the download icon (circled in red) to bring up a pop up dialog. Click **Zip Archive** (red arrow) to
   accept the usage agreement and download the dataset

    .. image:: images/0.6imagedownload_paclitaxel.png
        :alt: CM4AI February 2025 data release paclitaxel circled in red

    .. note::

        For **vorinostat** dataset, look for **cm4ai-v0.6-beta-if-images-vorinostat.zip** entry and perform the same
        operations above. Same goes for untreated, look for **cm4ai-v0.6-beta-if-images-untreated.zip**

#. Unzip file

    This can be done by double clicking on the file or if on a Mac/Linux machine by running the following
    on a command line:

    .. code-block::

        unzip cm4ai-v0.6-beta-if-images-paclitaxel.zip


#. Running cellmaps_pipelinecmd command

    .. code-block::

        # Be sure to unzip the zip file above before running this step
        cellmaps_imagedownloadercmd.py ./paclitaxel_image  \
            --cm4ai_table paclitaxel/manifest.csv  \
            --provenance examples/provenance.json

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
