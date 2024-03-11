=============================================
What is and how to create a provenance file
=============================================

A provenance file is a `JSON`_ formatted file that contains information describing
sources of input data fed into the `cellmaps_pipeline`_. It is required to maintain
a chain of history for `FAIRSCAPE`_

Template provenance file:

.. code-block:: python

    {
      "name": "Name for pipeline run",
      "organization-name": "Name of lab or group. Ex: Ideker",
      "project-name": "Name of funding source or project",
      "cell-line": "Name of cell line. Ex: U2OS",
      "treatment": "Name of treatment, Ex: untreated",
      "release": "Name of release. Example: 0.1 alpha",
      "gene-set": "Name of gene set. Example chromatin",
      "edgelist": {
        "name": "Name of dataset",
        "author": "Author of dataset",
        "version": "Version of dataset",
        "date-published": "Date dataset was published",
        "description": "Description of dataset",
        "data-format": "Format of data"
      },
      "baitlist": {
        "name": "Name of dataset",
        "author": "Author of dataset",
        "version": "Version of dataset",
        "date-published": "Date dataset was published",
        "description": "Description of dataset",
        "data-format": "Format of data"
      },
      "samples": {
        "name": "Name of dataset",
        "author": "Author of dataset",
        "version": "Version of dataset",
        "date-published": "Date dataset was published",
        "description": "Description of dataset",
        "data-format": "Format of data"
      },
      "unique": {
        "name": "Name of dataset",
        "author": "Author of dataset",
        "version": "Version of dataset",
        "date-published": "Date dataset was published",
        "description": "Description of dataset",
        "data-format": "Format of data"
      }
    }




The above template provenance file can be created a few ways:

**By** grabbing the `JSON`_ test from help output from `cellmaps_pipelinecmd.py` like so:

.. code-block:: python

    cellmaps_pipelinecmd.py -h

**Or** by directly writing the `JSON`_ to a file
(in example below it is writing to `provenance.json`)
via this command line invocation:

.. code-block:: python

    cellmaps_pipelinecmd.py . --example_provenance > provenance.json


**Or**, if input datasets are already registered with FAIRSCAPE

TODO

.. note::

    FAIRSCAPE registration documentation is coming soon...

.. _CM4AI data: https://cm4ai.org/data
.. _RO-Crate: https://www.researchobject.org/ro-crate/
.. _Human Protein Atlas: https://www.proteinatlas.org
.. _Bioplex: https://bioplex.hms.harvard.edu
.. _cellmaps_pipeline: https://github.com/idekerlab/cellmaps_pipeline
.. _JSON: https://www.json.org/json-en.html
.. _FAIRSCAPE: https://fairscape.github.io
