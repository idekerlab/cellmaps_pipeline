#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_pipeline` package."""
import unittest

from cellmaps_imagedownloader.exceptions import CellMapsImageDownloaderError

from cellmaps_pipeline.runner import ProgrammaticPipelineRunner
import os
import shutil
from unittest.mock import patch, MagicMock


class TestProgrammaticPipelineRunner(unittest.TestCase):

    def setUp(self):
        self.outdir = './temp_dir'
        self.runner = ProgrammaticPipelineRunner(outdir=self.outdir)

    def tearDown(self):
        if os.path.exists(self.outdir):
            shutil.rmtree(self.outdir)

    @patch("os.path.isdir", return_value=False)
    def test_image_download_missing_parameters(self, mock_isdir):
        self.runner._cm4ai_image = None
        self.runner._samples = None
        self.runner._unique = None
        with self.assertRaises(CellMapsImageDownloaderError):
            self.runner._download_images()


if __name__ == '__main__':
    unittest.main()
