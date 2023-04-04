#! /usr/bin/env python

import os
import logging
import time
from cellmaps_utils import cellmaps_io
import cellmaps_pipeline
from cellmaps_pipeline.exceptions import CellmapsPipelineError


logger = logging.getLogger(__name__)


class CellmapsPipelineRunner(object):
    """
    Class to run algorithm
    """
    def __init__(self, outdir=None):
        """
        Constructor

        :param exitcode: value to return via :py:meth:`.CellmapsPipelineRunner.run` method
        :type int:
        """
        self._outdir = outdir
        self._start_time = int(time.time())
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

        cellmaps_io.setup_filelogger(outdir=self._outdir,
                                     handlerprefix='cellmaps_pipeline')
        cellmaps_io.write_task_start_json(outdir=self._outdir,
                                          start_time=self._start_time,
                                          version=cellmaps_pipeline.__version__)

        exit_status = 99
        try:
            exit_status = 0
        finally:
            cellmaps_io.write_task_finish_json(outdir=self._outdir,
                                               start_time=self._start_time,
                                               status=exit_status)
        return exit_status
