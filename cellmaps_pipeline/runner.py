#! /usr/bin/env python

import os
import sys
import warnings
import logging
import time
import networkx as nx
from cellmaps_utils import logutils
from cellmaps_utils import constants

from cellmaps_imagedownloader.runner import MultiProcessImageDownloader
from cellmaps_imagedownloader.runner import FakeImageDownloader
from cellmaps_imagedownloader.runner import CellmapsImageDownloader
from cellmaps_imagedownloader.gene import ImageGeneNodeAttributeGenerator
from cellmaps_ppidownloader.runner import CellmapsPPIDownloader
from cellmaps_ppidownloader.gene import APMSGeneNodeAttributeGenerator
from cellmaps_ppi_embedding.runner import Node2VecEmbeddingGenerator
from cellmaps_ppi_embedding.runner import CellMapsPPIEmbedder
from cellmaps_image_embedding.runner import CellmapsImageEmbedder
from cellmaps_image_embedding.runner import FakeEmbeddingGenerator
from cellmaps_image_embedding.runner import DensenetEmbeddingGenerator
from cellmaps_coembedding.runner import MuseCoEmbeddingGenerator
from cellmaps_coembedding.runner import FakeCoEmbeddingGenerator
from cellmaps_coembedding.runner import CellmapsCoEmbedder
from cellmaps_generate_hierarchy.ppi import CosineSimilarityPPIGenerator
from cellmaps_generate_hierarchy.hierarchy import CDAPSHierarchyGenerator
from cellmaps_generate_hierarchy.runner import CellmapsGenerateHierarchy

import cellmaps_pipeline
from cellmaps_pipeline.exceptions import CellmapsPipelineError


logger = logging.getLogger(__name__)


class PipelineRunner(object):
    """
    Base command runner
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    def run(self):
        """
        Runs pipeline
        :param cmd:
        :raises NotImplementedError: Always raised cause
                                     subclasses need to implement
        """
        raise NotImplementedError('subclasses need to implement')


class ProgrammaticPipelineRunner(PipelineRunner):
    """

    """
    def __init__(self, outdir=None,
                 samples=None,
                 unique=None,
                 edgelist=None,
                 baitlist=None,
                 model_path=None,
                 fake=None,
                 provenance=None,
                 input_data_dict=None):
        """
        Constructor
        """
        super().__init__()
        self._outdir = os.path.abspath(outdir)
        self._samples = samples
        self._unique = unique
        self._edgelist = edgelist
        self._baitlist = baitlist
        self._model_path = model_path
        self._fake = fake
        self._provenance = provenance
        self._input_data_dict = input_data_dict
        self._image_dir = os.path.join(self._outdir,
                                       constants.IMAGE_DOWNLOAD_STEP_DIR)
        self._ppi_dir = os.path.join(self._outdir,
                                     constants.PPI_DOWNLOAD_STEP_DIR)
        self._ppi_embed_dir = os.path.join(self._outdir,
                                           constants.PPI_EMBEDDING_STEP_DIR)
        self._image_embed_dir = os.path.join(self._outdir,
                                             constants.IMAGE_EMBEDDING_STEP_DIR)
        self._coembed_dir = os.path.join(self._outdir,
                                         constants.COEMBEDDING_STEP_DIR)

        self._hierarchy_dir = os.path.join(self._outdir,
                                           constants.HIERARCHY_STEP_DIR)

    def run(self):
        """
        Runs pipeline programmatically in serial steps. This would
        be the same as running the steps in a notebook

        :raises CellmapsPipelineError: if command returns non zero value

        """
        if self._download_images() != 0:
            raise CellmapsPipelineError('Image download failed')

        if self._download_ppi() != 0:
            raise CellmapsPipelineError('PPI download failed')

        if self._embed_ppi() != 0:
            raise CellmapsPipelineError('PPI embed failed')

        if self._embed_image() != 0:
            raise CellmapsPipelineError('Image embed failed')

        if self._coembed() != 0:
            raise CellmapsPipelineError('Coembed failed')

        if self._hierarchy() != 0:
            raise CellmapsPipelineError('Hierarchy failed')

        return 0

    def _hierarchy(self):
        """

        :return:
        """
        if self._fake is True and os.path.isdir(self._hierarchy_dir):
            warnings.warn('Found hierarchy dir, assuming we are good. skipping')
            return 0

        ppigen = CosineSimilarityPPIGenerator(embeddingdir=self._coembed_dir)

        hiergen = CDAPSHierarchyGenerator()
        return CellmapsGenerateHierarchy(outdir=self._hierarchy_dir,
                                         inputdir=self._coembed_dir,
                                         ppigen=ppigen,
                                         hiergen=hiergen,
                                         input_data_dict=self._input_data_dict).run()

    def _coembed(self):
        """

        :return:
        """
        if self._fake is True and os.path.isdir(self._coembed_dir):
            warnings.warn('Found coembedding dir, assuming we are good. skipping')
            return 0

        if self._fake:
            gen = FakeCoEmbeddingGenerator(ppi_embeddingdir=self._ppi_embed_dir,
                                           image_embeddingdir=self._image_embed_dir,
                                           image_downloaddir=self._image_dir)
        else:
            gen = MuseCoEmbeddingGenerator(outdir=self._coembed_dir,
                                           ppi_embeddingdir=self._ppi_embed_dir,
                                           image_embeddingdir=self._image_embed_dir,
                                           image_downloaddir=self._image_dir)
        return CellmapsCoEmbedder(outdir=self._coembed_dir,
                                  inputdirs=[self._image_embed_dir, self._ppi_embed_dir,
                                             self._image_dir],
                                  embedding_generator=gen,
                                  input_data_dict=self._input_data_dict).run()

    def _embed_image(self):
        """

        :return:
        """
        if self._fake is True and os.path.isdir(self._image_embed_dir):
            warnings.warn('Found image embedding dir, assuming we are good. skipping')
            return 0

        if self._fake is True:
            gen = FakeEmbeddingGenerator(self._image_dir)
        else:
            gen = DensenetEmbeddingGenerator(self._image_dir,
                                             outdir=self._image_embed_dir,
                                             model_path=self._model_path)
        return CellmapsImageEmbedder(outdir=self._image_embed_dir,
                                     inputdir=self._image_dir,
                                     embedding_generator=gen,
                                     input_data_dict=self._input_data_dict).run()

    def _embed_ppi(self):
        """

        :return:
        """
        if self._fake is True and os.path.isdir(self._ppi_embed_dir):
            warnings.warn('Found ppi embedding dir, assuming we are good. skipping')
            return 0
        gen = Node2VecEmbeddingGenerator(
            nx_network=nx.read_edgelist(CellMapsPPIEmbedder.get_apms_edgelist_file(self._ppi_dir),
                                        delimiter='\t'))

        return CellMapsPPIEmbedder(outdir=self._ppi_embed_dir,
                                   embedding_generator=gen,
                                   inputdir=self._ppi_dir,
                                   input_data_dict=self._input_data_dict).run()

    def _download_ppi(self):
        """

        :return:
        """
        if self._fake is True and os.path.isdir(self._ppi_dir):
            warnings.warn('Found ppi dir, assuming we are good. skipping')
            return 0
        apmsgen = APMSGeneNodeAttributeGenerator(
            apms_edgelist=APMSGeneNodeAttributeGenerator.get_apms_edgelist_from_tsvfile(self._edgelist),
            apms_baitlist=APMSGeneNodeAttributeGenerator.get_apms_baitlist_from_tsvfile(self._baitlist))

        return CellmapsPPIDownloader(outdir=self._ppi_dir,
                                     apmsgen=apmsgen,
                                     input_data_dict=self._input_data_dict,
                                     provenance=self._provenance).run()

    def _download_images(self):
        """
        Downloads Images using
        :py:class:`~cellmaps_imagedownloader.runner.CellmapsImageDownloader`

        :return: exit code of :py:meth:`~cellmaps_imagedownloader.runner.CellmapsImageDownloader.run`
        :rtype: int
        """
        if self._fake is True and os.path.isdir(self._image_dir):
            warnings.warn('Found image dir, assuming we are good. skipping')
            return 0
        logger.info('Downloading images')
        imagegen = ImageGeneNodeAttributeGenerator(
            unique_list=ImageGeneNodeAttributeGenerator.get_unique_list_from_csvfile(self._unique),
            samples_list=ImageGeneNodeAttributeGenerator.get_samples_from_csvfile(self._samples))

        if self._fake is True:
            warnings.warn('FAKE IMAGES ARE BEING DOWNLOADED!!!!!')
            dloader = FakeImageDownloader()
        else:
            dloader = MultiProcessImageDownloader()
        # Todo: input_data_dict should NOT be required to run this
        #       https://github.com/idekerlab/cellmaps_imagedownloader/issues/2
        return CellmapsImageDownloader(outdir=self._image_dir,
                                       imagedownloader=dloader,
                                       imagegen=imagegen,
                                       provenance=self._provenance,
                                       input_data_dict=self._input_data_dict).run()


class CellmapsPipeline(object):
    """
    Class to run algorithm
    """
    def __init__(self, outdir=None,
                 runner=None,
                 input_data_dict=None):
        """
        Constructor

        :param exitcode: value to return via :py:meth:`.CellmapsPipeline.run` method
        :type int:
        """
        if outdir is None:
            raise CellmapsPipelineError('outdir is None')

        self._outdir = os.path.abspath(outdir)
        self._start_time = int(time.time())
        self._runner = runner
        self._input_data_dict = input_data_dict
        logger.debug('In constructor')

    def run(self):
        """
        Runs CM4AI Pipeline


        :return:
        """
        logger.debug('In run method')
        if self._outdir is None:
            raise CellmapsPipelineError('outdir must be set')

        if not os.path.isdir(self._outdir):
            os.makedirs(self._outdir, mode=0o755)

        logutils.write_task_start_json(outdir=self._outdir,
                                       start_time=self._start_time,
                                       data={'commandlineargs': self._input_data_dict},
                                       version=cellmaps_pipeline.__version__)

        exit_status = 99
        try:
            exit_status = self._runner.run()
        finally:
            logutils.write_task_finish_json(outdir=self._outdir,
                                            start_time=self._start_time,
                                            status=exit_status)
        return exit_status
