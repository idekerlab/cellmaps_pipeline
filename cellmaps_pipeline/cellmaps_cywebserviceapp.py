#! /usr/bin/env python

import argparse
import json
import os.path
import math
import sys
import numpy as np
import pandas as pd
import logging
import logging.config

from cellmaps_utils import logutils
from cellmaps_utils import constants
from cellmaps_utils import music_utils

from ndex2.cx2 import CX2Network

import cellmaps_pipeline


logger = logging.getLogger(__name__)


def _parse_arguments(desc, args):
    """
    Parses command line arguments

    :param desc: description to display on command line
    :type desc: str
    :param args: command line arguments usually :py:func:`sys.argv[1:]`
    :type args: list
    :return: arguments parsed by :py:mod:`argparse`
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=constants.ArgParseFormatter)
    parser.add_argument('input', help='Input data')
    parser.add_argument('--mode', required=True,
                        choices=['networkfromembedding',
                                 'communitydetection',
                                 'createhcx'],
                        help='Action to perform')
    parser.add_argument('--embedding',
                        help='Sets the embedding file to load. Used by --mode networkfromebedding')
    parser.add_argument('--similarity',
                        choices=['euclidean', 'cosine', 'manhatten',
                                 'canberra', 'pearson', 'spearman', 'kendall'], default='cosine',
                        help='Sets type of similarity algorithm to use during embedding'
                             'conversion')
    parser.add_argument('--embedding_cutoff', default=0.1, type=float,
                        help='Cutoff for keeping embedding edges, 0.0 means keep all edges,'
                             '0.1 means keep top 10 percent')
    parser.add_argument('--tempdir', default='/tmp',
                        help='Directory needed to hold files temporarily for processing')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat '
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')
    parser.add_argument('--verbose', '-v', action='count', default=3,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module. Messages are '
                             'output at these python logging levels '
                             '-v = WARNING, -vv = INFO, '
                             '-vvv = DEBUG, -vvvv = NOTSET (default ERROR '
                             'logging)')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 cellmaps_pipeline.__version__))

    return parser.parse_args(args)

def _get_sim_mat_from_similarity(df=None, algorithm='cosine'):
    """

    :param df:
    :param similarity_measurement:
    :return:
    """
    if algorithm is None:
        raise Exception('similarity measurement is None')

    alorithm_lower = algorithm.lower()
    if alorithm_lower == 'cosine':
        return music_utils.cosine_similarity_scaled(df)
    elif alorithm_lower == 'manhattan':
        return music_utils.manhattan_similarity(df)
    elif alorithm_lower == 'pearson':
        return music_utils.pearson_scaled(df)
    elif alorithm_lower == 'kendall':
        return music_utils.kendall_scaled(df)
    elif alorithm_lower == 'euclidean':
        return music_utils.euclidean_similarity(df)
    elif alorithm_lower == 'canberra':
        return music_utils.canberra_similarity(df)
    elif alorithm_lower == 'spearman':
        return music_utils.spearman_scaled(df)

    raise Exception('Invalid similarity: ' + str(algorithm))

def network_from_embedding_mode(embedding=None, algorithm='cosine',
                                cutoff=0.1):
    df = pd.read_table(embedding, sep='\t', index_col=0)

    sim_mat = _get_sim_mat_from_similarity(df=df,
                                           algorithm=algorithm)

    keep = np.triu(np.ones(sim_mat.shape)).astype(bool)
    sim_mat = sim_mat.where(keep)

    pairs = sim_mat.stack().reset_index().rename(columns={'level_0': constants.PPI_EDGELIST_GENEA_COL,
                                                          'level_1': constants.PPI_EDGELIST_GENEB_COL,
                                                          0: constants.WEIGHTED_PPI_EDGELIST_WEIGHT_COL})

    pairs = pairs[pairs[constants.PPI_EDGELIST_GENEA_COL] != pairs[constants.PPI_EDGELIST_GENEB_COL]]
    edgelist = pairs.sort_values(constants.WEIGHTED_PPI_EDGELIST_WEIGHT_COL, ascending=False)

    edgelist_cutoff = edgelist.iloc[0:math.ceil(cutoff * len(edgelist))]

    new_net = CX2Network()
    new_net.add_network_attribute(key="name", value="fake network")
    node_id1 = new_net.add_node(attributes={"name": "node1"})
    node_id2 = new_net.add_node(attributes={"name": "node2"})
    new_net.add_edge(source=node_id1, target=node_id2)
    return [new_net.to_cx2()]

def main(args):
    """
    Main entry point for program.
    The Cell Maps Pipeline cywebserviceapp provides a wrapper to support invocation
    of tools as Cytoscape Web Service Apps

    The result of this invocation is written to standard out

    :param args: arguments passed to command line usually :py:func:`sys.argv[1:]`
    :type args: list

    :return: return value of 0 upon success otherwise failure
    :rtype: int
    """

    desc = r"""
Version {version}

The Cell Maps Pipeline cywebserviceapp provides a wrapper to support invocation
of tools as Cytoscape Web Service Apps


For more information visit https://cellmaps-pipeline.readthedocs.io
    """.format(version=cellmaps_pipeline.__version__)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = cellmaps_pipeline.__version__
    result = {}
    try:

        logutils.setup_cmd_logging(theargs)
        if theargs.mode == 'networkfromembedding':
            result = [{'action': 'addNetworks',
                       'data': network_from_embedding_mode(embedding=theargs.embedding,
                                                           algorithm=theargs.similarity,
                                                           cutoff=theargs.embedding_cutoff,
                                                           )}]
        json.dump(result, sys.stdout, indent=2)
    except Exception as e:
        logger.exception('Caught exception: ' + str(e))
        return 2
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
