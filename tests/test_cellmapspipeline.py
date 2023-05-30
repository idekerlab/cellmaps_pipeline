#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_pipeline` package."""


import unittest
from cellmaps_pipeline.runner import CellmapsPipeline
from cellmaps_pipeline.exceptions import CellmapsPipelineError


class TestCellmapspipelinerunner(unittest.TestCase):
    """Tests for `cellmaps_pipeline` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_constructor(self):
        """Tests constructor"""
        myobj = CellmapsPipeline('foo')

        self.assertIsNotNone(myobj)

    def test_run_outdir_not_set(self):
        """ Tests run()"""
        try:
            myobj = CellmapsPipeline()
            myobj.run()
            self.fail('expected exception')
        except CellmapsPipelineError as e:
            self.assertEqual('outdir is None', str(e))
