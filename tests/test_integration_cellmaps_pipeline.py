#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration Tests for `cellmaps_pipeline` package."""

import os
import sys
import json
import tempfile
import unittest
import shutil
from cellmaps_pipeline.runner import ProgrammaticPipelineRunner
from cellmaps_pipeline.runner import CellmapsPipeline

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

    def get_examples_dir(self):
        return os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), 'examples')

    def test_usage_example_takes_thirty_minutes(self):
        temp_dir = tempfile.mkdtemp()
        try:
            sys.stdout.write('Temp directory for test_usage_example_takes_thirty_minutes(): ' + str(temp_dir))
            sys.stdout.flush()
            # load the provenance as a dict
            with open(os.path.join('examples', 'provenance.json'), 'r') as f:
                json_prov = json.load(f)
            example_dir = self.get_examples_dir()
            outdir = os.path.join(temp_dir, 'myrun')
            runner = ProgrammaticPipelineRunner(outdir=outdir,
                                                samples=os.path.join(example_dir, 'samples.csv'),
                                                unique=os.path.join(example_dir, 'unique.csv'),
                                                edgelist=os.path.join(example_dir, 'edgelist.tsv'),
                                                baitlist=os.path.join(example_dir, 'baitlist.tsv'),
                                                provenance=json_prov,
                                                ppi_cutoffs=[0.001, 0.01],
                                                input_data_dict={})

            pipeline = CellmapsPipeline(outdir=outdir,
                                        runner=runner,
                                        input_data_dict={})
            self.assertEqual(0, pipeline.run())
        finally:
            sys.stdout.write('Removing temp directory for test_usage_example_takes_thirty_minutes(): ' + str(temp_dir))
            shutil.rmtree(temp_dir)
