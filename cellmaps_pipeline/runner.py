#! /usr/bin/env python

import os
import warnings
import logging
import time
import networkx as nx
from cellmaps_utils import logutils
from cellmaps_utils import constants
from cellmaps_utils.provenance import ProvenanceUtil

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
from cellmaps_generate_hierarchy.hierarchy import CDAPSHiDeFHierarchyGenerator
from cellmaps_generate_hierarchy.maturehierarchy import HiDeFHierarchyRefiner
from cellmaps_generate_hierarchy.runner import CellmapsGenerateHierarchy
from cellmaps_imagedownloader.proteinatlas import ProteinAtlasReader
from cellmaps_imagedownloader.proteinatlas import ProteinAtlasImageUrlReader
from cellmaps_imagedownloader.proteinatlas import ImageDownloadTupleGenerator

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
                 proteinatlasxml=None,
                 ppi_cutoffs=None,
                 fake=None,
                 provenance=None,
                 provenance_utils=ProvenanceUtil(),
                 fold=1,
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
        self._provenance_utils = provenance_utils
        self._fold = fold
        self._proteinatlasxml = proteinatlasxml
        self._ppi_cutoffs = ppi_cutoffs
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
        if os.path.isdir(self._hierarchy_dir):
            warnings.warn('Found hierarchy dir, assuming we are good. skipping')
            return 0

        ppigen = CosineSimilarityPPIGenerator(embeddingdir=self._coembed_dir,
                                              cutoffs=self._ppi_cutoffs)

        refiner = HiDeFHierarchyRefiner(provenance_utils=self._provenance_utils)

        hiergen = CDAPSHiDeFHierarchyGenerator(refiner=refiner,
                                               provenance_utils=self._provenance_utils)
        return CellmapsGenerateHierarchy(outdir=self._hierarchy_dir,
                                         inputdir=self._coembed_dir,
                                         ppigen=ppigen,
                                         hiergen=hiergen,
                                         input_data_dict=self._input_data_dict,
                                         provenance_utils=self._provenance_utils).run()

    def _coembed(self):
        """

        :return:
        """
        if os.path.isdir(self._coembed_dir):
            warnings.warn('Found coembedding dir, assuming we are good. skipping')
            return 0

        if self._fake:
            gen = FakeCoEmbeddingGenerator(ppi_embeddingdir=self._ppi_embed_dir,
                                           image_embeddingdir=self._image_embed_dir)
        else:
            gen = MuseCoEmbeddingGenerator(outdir=self._coembed_dir,
                                           ppi_embeddingdir=self._ppi_embed_dir,
                                           image_embeddingdir=self._image_embed_dir)
        return CellmapsCoEmbedder(outdir=self._coembed_dir,
                                  inputdirs=[self._image_embed_dir, self._ppi_embed_dir],
                                  embedding_generator=gen,
                                  input_data_dict=self._input_data_dict).run()

    def _embed_image(self):
        """

        :return:
        """
        if os.path.isdir(self._image_embed_dir):
            warnings.warn('Found image embedding dir, assuming we are good. skipping')
            return 0

        if self._fake is True:
            gen = FakeEmbeddingGenerator(self._image_dir)
        else:
            gen = DensenetEmbeddingGenerator(self._image_dir,
                                             outdir=self._image_embed_dir,
                                             model_path=self._model_path,
                                             fold=self._fold)
        return CellmapsImageEmbedder(outdir=self._image_embed_dir,
                                     inputdir=self._image_dir,
                                     embedding_generator=gen,
                                     input_data_dict=self._input_data_dict).run()

    def _embed_ppi(self):
        """

        :return:
        """
        if os.path.isdir(self._ppi_embed_dir):
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
        if os.path.isdir(self._ppi_dir):
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
        if os.path.isdir(self._image_dir):
            warnings.warn('Found image dir, assuming we are good. skipping')
            return 0
        logger.info('Downloading images')

        imagegen = ImageGeneNodeAttributeGenerator(
            unique_list=ImageGeneNodeAttributeGenerator.get_unique_list_from_csvfile(self._unique),
            samples_list=ImageGeneNodeAttributeGenerator.get_samples_from_csvfile(self._samples))

        proteinatlas_reader = ProteinAtlasReader(self._image_dir, proteinatlas=self._proteinatlasxml)
        proteinatlas_urlreader = ProteinAtlasImageUrlReader(reader=proteinatlas_reader)
        imageurlgen = ImageDownloadTupleGenerator(reader=proteinatlas_urlreader,
                                                  samples_list=imagegen.get_samples_list())

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
                                       imageurlgen=imageurlgen,
                                       provenance=self._provenance,
                                       skip_failed=True,
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
