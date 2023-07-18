===================
Cell Maps Pipeline
===================


.. image:: https://img.shields.io/pypi/v/cellmaps_pipeline.svg
        :target: https://pypi.python.org/pypi/cellmaps_pipeline

.. image:: https://img.shields.io/travis/idekerlab/cellmaps_pipeline.svg
        :target: https://travis-ci.com/idekerlab/cellmaps_pipeline

Cell Maps Pipeline for `Cell Maps for AI (CM4AI) <https://cm4ai.org>`__

The Cell Maps Pipeline takes ImmunoFluorescent images from the `Human Protein Atlas <https://www.proteinatlas.org>`__ along with
Affinity Purification Mass Spectrometry data from one or more sources, converts them into embeddings that
are then coembedded and converted into a Protein to Protein Interaction network from which a hierarchical
model is derived.

The pipeline invokes six tools that each create an output directory where results are
stored and registered within `Research Object Crates (RO-Crate) <https://www.researchobject.org/ro-crate>`__ using
the `FAIRSCAPE-cli <https://pypi.org/project/fairscape-cli>`__.

Overview of Cell Maps Pipeline

.. image:: images/pipeline_overview.png
  :alt: Overview of Cell Maps Pipeline which shows PPI and image download followed by embedding, coembedding, and finally hierarchy generation



* Free software: MIT license

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   modules
   developer
   authors
   history

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
