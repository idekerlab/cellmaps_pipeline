Creating a new release
===========================

This is an advanced developer section that describes creation of a new release for cellmaps_pipeline and deploying
that release onto PyPi_

.. note::

    THESE INSTRUCTIONS ARE FOR DOING A RELEASE ONLY AND NOT FOR REGULAR COMMITS

.. warning::

    **Releases should be done from main_ branch**

Testing
--------

Before deploy verify code is working by invoking:

.. code-block::

    make coverage

The above command runs the unit tests and calculates code coverage of the unit tests.

To just run tests:

.. code-block::

    make test

All tests should pass

.. code-block::

    make lint

Lint should not complain

.. note::

    To run tests that exercise the enter package see :doc:`integrationtesting`

Committing code
-------------------

Before doing a release, the code must be assigned a new :ref:`versioningscheme:Versioning Scheme`

First run **git tag** to find the latest version. Pick the next highest version number. The tags in github start with v because versions cannot start with numeric value.

**git tag example:**

.. code-block::

    $ git tag
    v0.2.0
    v0.3.0
    v0.4.0

.. note::

    Versions should adhere to this :ref:`versioningscheme:Versioning Scheme`

Be sure to update the version in ``cellmaps_pipeline/__init__.py`` Omit the ``v`` when setting the version in the file.

Commit the above changes and push to **main**:

.. code-block::

    git commit -m 'message...' cellmaps_pipeline/__init__.py
    git push origin main

Tagging code
----------------

Now tag source with version:

.. code-block::

    git tag -a v0.4.0 -m 'Information describing release'

Push the tag to github:

.. code-block::

    git push origin v0.4.0

Verify unit tests pass on Travis_
-----------------------------------

Click on this link Travis_ and verify unit tests are passing for the new version committed in the previous step. If not fix issues and start over at the top.

The tag should be visible from github now. If not something is wrong.

Create distributable binaries
--------------------------------

From cellmaps_pipeline source tree generate the wheel and tar.gz files

.. code-block::

    make dist

Under ``dist/`` will be files such as these:

.. code-block::

    $ tree
    dist
    |-- cellmaps_pipeline-0.1.0-py2.py3-none-any.whl
    `-- cellmaps_pipeline-0.1.0.tar.gz

Documenting release on Github
--------------------------------

Be sure to add release notes to HISTORY.rst file in source tree and be sure the text is in restructured text format otherwise it will fail to install on PyPI. To check text paste it into this site

#. From https://github.com/idekerlab/cellmaps_pipeline click on releases link.
#. Click on the Draft a new release button.
#. In the Tag version field select the version set above.
#. Enter a release title and describe changes in release copying notes put into HISTORY.rst.
#. Attach distributable binaries created above to release via the Attach binaries link on the page.
#. Click publish release.
#. Deploy to test pypi
#. First deploy to pypi test server by running this:

    .. code-block::

        make testrelease

    .. note::

        The above requires one to have accounts on Test PyPI serverand a credential file setup in your home directory. See :doc:`pypircfile` for more information.

Once the above is done verify deploy was successful by browsing to https://testpypi.python.org/pypi/cellmaps_pipeline and verifying new release was deployed.

Also test the package by installing it locally by running this:

.. code-block::

    pip install -i https://testpypi.python.org/pypi cellmaps_pipeline

.. note::

    If there is a problem a new version will need to be tagged in source tree cause pypi does not allow updating of deployed versions.

Deploy to PyPi_
------------------

If the above works perform the formal release by running:

.. code-block::

    make release

.. note::

    The above requires one to have accounts on PyPi_ server and a credential file setup in your home directory. See :doc:`pypircfile` for more information.

.. code-block::

    pip install cellmaps_pipeline


.. _Travis: https://travis-ci.org/idekerlab/cellmaps_pipeline
.. _main: https://github.com/idekerlab/cellmaps_pipeline/tree/main
.. _PyPi: https://pypi.org
.. _TestPyPi: https://test.pypi.org
