#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_pipeline` package."""
import unittest
import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock

from cellmaps_utils import constants

from cellmaps_pipeline.runner import PipelineRunner
from cellmaps_pipeline.exceptions import CellmapsPipelineError


class TestPipelineRunner(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        try:
            runner = PipelineRunner('foo')
            runner.run()
            self.fail('Expected NotImplementedError')
        except NotImplementedError as e:
            self.assertTrue('subclasses need to implement' in str(e))

    def test_get_image_coembed_tuples_fold_is_none(self):
        runner = PipelineRunner('foo')
        try:
            runner._get_image_coembed_tuples(None)
            self.fail('Expected CellmapsPipelineError')
        except CellmapsPipelineError as e:
            self.assertTrue('Fold cannot be None' in str(e))

    def test_get_image_coembed_tuples_fold_single_entry(self):
        temp_dir = tempfile.mkdtemp()
        try:
            runner = PipelineRunner(temp_dir)
            coembed_tuples = runner._get_image_coembed_tuples([1])
            self.assertEqual(1, coembed_tuples[0][0])
            self.assertEqual(os.path.join(temp_dir, constants.IMAGE_EMBEDDING_STEP_DIR + '1'),
                             coembed_tuples[0][1])
            self.assertEqual(os.path.join(temp_dir, constants.COEMBEDDING_STEP_DIR + '1'),
                             coembed_tuples[0][2])
        finally:
            shutil.rmtree(temp_dir)

    def test_get_image_coembed_tuples_fold_multiple_entry(self):
        temp_dir = tempfile.mkdtemp()
        try:
            runner = PipelineRunner(temp_dir)
            coembed_tuples = runner._get_image_coembed_tuples([1, 2])
            for entry in [1, 2]:
                print(coembed_tuples)
                self.assertEqual(entry, coembed_tuples[entry-1][0])
                self.assertEqual(os.path.join(temp_dir,
                                              constants.IMAGE_EMBEDDING_STEP_DIR +
                                              str(entry)),
                                 coembed_tuples[entry-1][1])
                self.assertEqual(os.path.join(temp_dir,
                                              constants.COEMBEDDING_STEP_DIR +
                                              str(entry)),
                                 coembed_tuples[entry-1][2])
        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    unittest.main()
