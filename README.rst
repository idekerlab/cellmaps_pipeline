===================
Cell Maps Pipeline
===================


.. image:: https://img.shields.io/pypi/v/cellmaps_pipeline.svg
        :target: https://pypi.python.org/pypi/cellmaps_pipeline

.. image:: https://app.travis-ci.com/idekerlab/cellmaps_pipeline.svg?branch=main
        :target: https://app.travis-ci.com/idekerlab/cellmaps_pipeline

.. image:: https://readthedocs.org/projects/cellmaps-pipeline/badge/?version=latest
        :target: https://cellmaps-pipeline.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

* Free software: MIT license
* Documentation: https://cellmaps-pipeline.readthedocs.io.

Dependencies
------------

* `cellmaps_utils <https://pypi.org/project/cellmaps-utils>`__
* `cellmaps_imagedownloader <https://pypi.org/project/cellmaps-imagedownloader>`__
* `cellmaps_ppidownloader <https://pypi.org/project/cellmaps-ppidownloader>`__
* `cellmaps_image_embedding <https://pypi.org/project/cellmaps-image-embedding>`__
* `cellmaps_ppi_embedding <https://pypi.org/project/cellmaps-ppi-embedding/>`__
* `cellmaps_coembedding <https://pypi.org/project/cellmaps-coembedding>`__
* `cellmaps_generate_hierarchy <https://pypi.org/project/cellmaps-generate-hierarchy>`__
* `networkx <https://pypi.org/project/networkx>`__

Compatibility
-------------

* Python 3.8+

Installation
------------

.. code-block::

   git clone https://github.com/idekerlab/cellmaps_pipeline
   cd cellmaps_pipeline
   make dist
   pip install dist/cellmaps_pipeline*whl


Run **make** command with no arguments to see other build/deploy options including creation of Docker image 

.. code-block::

   make

Output:

.. code-block::

   clean                remove all build, test, coverage and Python artifacts
   clean-build          remove build artifacts
   clean-pyc            remove Python file artifacts
   clean-test           remove test and coverage artifacts
   lint                 check style with flake8
   test                 run tests quickly with the default Python
   test-all             run tests on every Python version with tox
   coverage             check code coverage quickly with the default Python
   docs                 generate Sphinx HTML documentation, including API docs
   servedocs            compile the docs watching for changes
   testrelease          package and upload a TEST release
   release              package and upload a release
   dist                 builds source and wheel package
   install              install the package to the active Python's site-packages
   dockerbuild          build docker image and store in local repository
   dockerpush           push image to dockerhub

For developers
-------------------------------------------

To deploy development versions of this package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below are steps to make changes to this code base, deploy, and then run
against those changes.

#. Make changes

   Modify code in this repo as desired

#. Build and deploy

.. code-block::

    # From base directory of this repo cellmaps_pipeline
    pip uninstall cellmaps_pipeline -y ; make clean dist; pip install dist/cellmaps_pipeline*whl



Needed files
------------

* samples file: CSV file with list of IF images to download (see sample samples file in examples folder)
* unique file: CSV file of unique samples (see sample unique file in examples folder)
* bait list file: TSV file of baits used for AP-MS experiments
* edge list file: TSV file of edges for protein interaction network
* provenance: file containing provenance information about input files in JSON format (see sample provenance file in examples folder)

Usage
-----

For information invoke :code:`cellmaps_pipelinecmd.py -h`

**Example usage**

.. code-block::

   cellmaps_pipelinecmd.py ./cellmaps_pipeline_outdir --samples examples/samples.csv --unique examples/unique.csv --edgelist examples/edgelist.tsv --baitlist examples/baitlist.tsv --provenance examples/provenance.json


Via Docker
~~~~~~~~~~~~~~~~~~~~~~

**Example usage**


.. code-block::

   Coming soon...

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _NDEx: http://www.ndexbio.org
