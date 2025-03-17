.. highlight:: shell

============
Installation
============


Stable release (option 1)
--------------------------

To install the Cell Maps Pipeline, run this command in your terminal:

.. code-block:: console

    $ pip install cellmaps_pipeline

**This is the preferred method to install Cell Maps Pipeline**, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

It is recommended to use conda environment with python 3.8+.

From sources (option 2)
------------------------

Alternatively, Cell Maps Pipeline can be installed from sources, which is particularly useful for customization
and development purposes. The sources for Cell Maps Pipeline can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone https://github.com/idekerlab/cellmaps_pipeline.git

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/idekerlab/cellmaps_pipeline/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

or use the Makefile:

.. code-block:: console

    $ make clean dist

.. note::
    Due to the large number of dependent packages, we suggest a virtual environment like Anaconda_
    set to Python_ 3.8 like so: ``conda create -n cellmaps_env python=3.8``


.. _Github repo: https://github.com/idekerlab/cellmaps_pipeline
.. _tarball: https://github.com/idekerlab/cellmaps_pipeline/tarball/master
.. _Python:  https://python.org
.. _Anaconda: https://www.anaconda.com
