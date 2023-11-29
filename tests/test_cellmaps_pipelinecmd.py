#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_pipeline` package."""

import os
import tempfile
import shutil

import unittest
from cellmaps_pipeline import cellmaps_pipelinecmd


class TestCellmaps_pipeline(unittest.TestCase):
    """Tests for `cellmaps_pipeline` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_parse_arguments(self):
        """Tests parse arguments"""
        res = cellmaps_pipelinecmd._parse_arguments('hi', ['outdir'])

        self.assertEqual(res.verbose, 1)
        self.assertEqual('outdir', res.outdir)
        self.assertEqual(res.logconf, None)

        someargs = ['-vv', '--logconf', 'hi', 'outdir']
        res = cellmaps_pipelinecmd._parse_arguments('hi', someargs)

        self.assertEqual(res.verbose, 3)
        self.assertEqual(res.logconf, 'hi')
        self.assertEqual('outdir', res.outdir)

    def test_main(self):
        """Tests main function"""

        # try where loading config is successful
        try:
            temp_dir = tempfile.mkdtemp()
            res = cellmaps_pipelinecmd.main(['myprog.py', 'outdir'])
            self.assertEqual(res, 1)
        finally:
            shutil.rmtree(temp_dir)
