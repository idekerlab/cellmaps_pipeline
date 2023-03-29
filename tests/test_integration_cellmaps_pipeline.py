#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration Tests for `cellmaps_pipeline` package."""

import os

import unittest
from cellmaps_pipeline import cellmaps_pipelinecmd

SKIP_REASON = 'CELLMAPS_PIPELINE_INTEGRATION_TEST ' \
              'environment variable not set, cannot run integration ' \
              'tests'

@unittest.skipUnless(os.getenv('CELLMAPS_PIPELINE_INTEGRATION_TEST') is not None, SKIP_REASON)
class TestIntegrationCellmaps_pipeline(unittest.TestCase):
    """Tests for `cellmaps_pipeline` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_something(self):
        """Tests parse arguments"""
        self.assertEqual(1, 1)
