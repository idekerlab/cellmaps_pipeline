===================
Cell Maps Pipeline
===================
**The Cell Maps Pipeline is part of the Cell Mapping Toolkit**

.. image:: https://img.shields.io/pypi/v/cellmaps_pipeline.svg
        :target: https://pypi.python.org/pypi/cellmaps_pipeline

.. image:: https://app.travis-ci.com/idekerlab/cellmaps_pipeline.svg?branch=main
        :target: https://app.travis-ci.com/idekerlab/cellmaps_pipeline

The Cell Maps Pipeline takes `ImmunoFluorescent <https://en.wikipedia.org/wiki/Immunofluorescence>`__ images from
the `Human Protein Atlas <https://www.proteinatlas.org>`__ along with
`Affinity Purification Mass Spectrometry <https://kroganlab.ucsf.edu/protein-protein-interaction-analysis>`__
data from one or more sources, converts them into embeddings that
are then coembedded and converted into an integrated interaction network from which a hierarchical
model is derived.

The pipeline invokes seven tools that each create an output directory where results are
stored and registered within `Research Object Crates (RO-Crate) <https://www.researchobject.org/ro-crate>`__ using
the `FAIRSCAPE-cli <https://pypi.org/project/fairscape-cli>`__.

**Overview of Cell Maps Pipeline**

.. image:: images/pipeline_overview.png
  :alt: Overview of Cell Maps Pipeline which shows PPI and image download followed by embedding, coembedding, and finally hierarchy generation

..
    The pipeline_overview.png image is from this google doc: https://docs.google.com/drawings/d/1pAqQkmg8hRh7ySkgu5PVY7Hu4pwMyejAzAYzGge0ilU/edit

* Free software: MIT license
* Source code: https://github.com/idekerlab/cellmaps_pipeline

Tools
^^^^^^

See links below for more information about the individual tools

* `cellmaps_imagedownloader <https://cellmaps-imagedownloader.readthedocs.io>`__
* `cellmaps_ppidownloader  <https://cellmaps-ppidownloader.readthedocs.io>`__
* `cellmaps_image_embedding <https://cellmaps-image-embedding.readthedocs.io>`__
* `cellmaps_ppi_embedding <https://cellmaps-ppi-embedding.readthedocs.io>`__
* `cellmaps_coembedding <https://cellmaps-coembedding.readthedocs.io>`__
* `cellmaps_generate_hierarchy <https://cellmaps-generate-hierarchy.readthedocs.io>`__
* `cellmaps_hierarchyeval <https://cellmaps-hierarchyeval.readthedocs.io>`__



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   outputs
   modules
   developer
   authors
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
