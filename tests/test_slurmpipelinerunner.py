#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_pipeline` package."""


import unittest
import tempfile
import shutil
import os
from cellmaps_pipeline.runner import SLURMPipelineRunner
from cellmaps_pipeline.exceptions import CellmapsPipelineError


class TestSLURMPipelineRunner(unittest.TestCase):
    """Tests for `cellmaps_pipeline` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_constructor(self):
        """Tests constructor"""
        myobj = SLURMPipelineRunner('foo')
        self.assertIsNotNone(myobj)

    def test_write_slurm_directives(self):
        temp_dir = tempfile.mkdtemp()
        try:
            myobj = SLURMPipelineRunner(temp_dir)
            filename = os.path.join(temp_dir, 'foo.txt')
            with open(filename, 'w') as f:
                myobj._write_slurm_directives(out=f)
            with open(filename, 'r') as f:
                data = f.read().split('\n')
            self.assertEqual('#!/bin/bash', data[0])
        finally:
            shutil.rmtree(temp_dir)
