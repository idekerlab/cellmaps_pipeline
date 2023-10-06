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

    def test_generate_download_images_command(self):
        temp_dir = tempfile.mkdtemp()
        cm4ai_image = 'test_image'
        provenance = 'test_provenance'
        try:
            myobj = SLURMPipelineRunner(temp_dir, cm4ai_image=cm4ai_image, provenance=provenance)
            filename = os.path.join(temp_dir, 'imagedownloadjob.sh')
            myobj._generate_download_images_command()
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)

    def test_generate_download_ppi_command(self):
        temp_dir = tempfile.mkdtemp()
        edgelist = 'edgelist'
        baitlist = 'baitlist'
        provenance = 'test_provenance'
        try:
            myobj = SLURMPipelineRunner(temp_dir, edgelist=edgelist, baitlist=baitlist, provenance=provenance)
            filename = os.path.join(temp_dir, 'ppidownloadjob.sh')
            myobj._generate_download_ppi_command()
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)

    def test_generate_embed_image_command(self):
        temp_dir = tempfile.mkdtemp()
        try:
            myobj = SLURMPipelineRunner(temp_dir)
            filename = os.path.join(temp_dir, 'imageembedjob1.sh')
            myobj._generate_embed_image_command()
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)

    def test_generate_embed_ppi_command(self):
        temp_dir = tempfile.mkdtemp()
        try:
            myobj = SLURMPipelineRunner(temp_dir)
            filename = os.path.join(temp_dir, 'ppiembedjob.sh')
            myobj._generate_embed_ppi_command()
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)

    def test_generate_coembed_command(self):
        temp_dir = tempfile.mkdtemp()
        try:
            myobj = SLURMPipelineRunner(temp_dir)
            filename = os.path.join(temp_dir, 'coembeddingjob1.sh')
            myobj._generate_coembed_command(fold=1)
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)

    def test_generate_hierarchy_command(self):
        temp_dir = tempfile.mkdtemp()
        try:
            myobj = SLURMPipelineRunner(temp_dir)
            filename = os.path.join(temp_dir, 'hierarchyjob.sh')
            myobj._generate_hierarchy_command()
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)

    def test_slurm_run(self):
        temp_dir = tempfile.mkdtemp()
        samples = 'test_samples'
        unique = 'test_unique'
        edgelist = 'edgelist'
        baitlist = 'baitlist'
        provenance = 'test_provenance'
        try:
            myobj = SLURMPipelineRunner(temp_dir, samples=samples, unique=unique,
                                        edgelist=edgelist, baitlist=baitlist, provenance=provenance)
            filename = os.path.join(temp_dir, 'slurm_cellmaps_job.sh')
            myobj.run()
            self.assertTrue(os.path.isfile(filename))
        finally:
            shutil.rmtree(temp_dir)
