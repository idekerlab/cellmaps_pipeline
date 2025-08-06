#! /usr/bin/env python

import argparse
import json
import os.path
import math
import sys
import tempfile

import cdapsutil
import numpy as np
import pandas as pd
import logging
import logging.config

from cellmaps_generate_hierarchy.hierarchy import CDAPSHiDeFHierarchyGenerator
from cellmaps_generate_hierarchy.maturehierarchy import HiDeFHierarchyRefiner
from cellmaps_generate_hierarchy.ppi import CosineSimilarityPPIGenerator
from cellmaps_generate_hierarchy.runner import CellmapsGenerateHierarchy
from cellmaps_utils import logutils
from cellmaps_utils import constants
from cellmaps_utils import music_utils

from ndex2.cx2 import CX2Network, RawCX2NetworkFactory, CX2NetworkPandasDataFrameFactory

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
    # TODO: what input supposed to be
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
    parser.add_argument('--interactome_uuid',
                        help='UUID of input NDEx network hierarchy')
    parser.add_argument('--ppi_cutoffs', nargs='+', type=float,
                        default=CosineSimilarityPPIGenerator.PPI_CUTOFFS,
                        help='Cutoffs used to generate PPI input networks. For example, '
                             'a value of 0.1 means to generate PPI input network using the '
                             'top ten percent of edges in interactome. Each cutoff generates '
                             'another PPI network')
    parser.add_argument('--k', default=CellmapsGenerateHierarchy.K_DEFAULT, type=int,
                        help='HiDeF stability parameter')
    parser.add_argument('--hidef_algorithm', default=CellmapsGenerateHierarchy.ALGORITHM,
                        help='HiDeF clustering algorithm parameter')
    parser.add_argument('--maxres', default=CellmapsGenerateHierarchy.MAXRES, type=float,
                        help='HiDeF max resolution parameter')
    parser.add_argument('--containment_threshold', default=HiDeFHierarchyRefiner.CONTAINMENT_THRESHOLD, type=float,
                        help='Containment index threshold for pruning hierarchy')
    parser.add_argument('--jaccard_threshold', default=HiDeFHierarchyRefiner.JACCARD_THRESHOLD, type=float,
                        help='Jaccard index threshold for merging similar clusters')
    parser.add_argument('--min_diff', default=HiDeFHierarchyRefiner.MIN_DIFF, type=float,
                        help='Minimum difference in number of proteins for every '
                             'parent-child pair')
    parser.add_argument('--min_system_size', default=HiDeFHierarchyRefiner.MIN_SYSTEM_SIZE, type=float,
                        help='Minimum number of proteins each system must have to be kept')
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
    new_net.add_network_attribute('name', f'Network from {os.path.basename(embedding)}')
    new_net.add_network_attribute('description', f'Created using {algorithm} similarity with top {cutoff:.0%} edges')

    node_to_id = {}
    for node in pd.unique(edgelist_cutoff[[constants.PPI_EDGELIST_GENEA_COL,
                                           constants.PPI_EDGELIST_GENEB_COL]].values.ravel()):
        node_to_id[node] = new_net.add_node(attributes={'name': node})

    for _, row in edgelist_cutoff.iterrows():
        src = node_to_id[row[constants.PPI_EDGELIST_GENEA_COL]]
        tgt = node_to_id[row[constants.PPI_EDGELIST_GENEB_COL]]
        weight = row[constants.WEIGHTED_PPI_EDGELIST_WEIGHT_COL]
        new_net.add_edge(source=src, target=tgt, attributes={'weight': weight})

    return [new_net.to_cx2()]


def community_detection_mode(interactome, ndex_uuid, ppi_cutoffs=CosineSimilarityPPIGenerator.PPI_CUTOFFS,
                             algorithm=CellmapsGenerateHierarchy.ALGORITHM, maxres=CellmapsGenerateHierarchy.MAXRES,
                             k=CellmapsGenerateHierarchy.K_DEFAULT,
                             containment_threshold=HiDeFHierarchyRefiner.CONTAINMENT_THRESHOLD,
                             jaccard_threshold=HiDeFHierarchyRefiner.JACCARD_THRESHOLD,
                             min_system_size=HiDeFHierarchyRefiner.MIN_SYSTEM_SIZE,
                             min_diff=HiDeFHierarchyRefiner.MIN_DIFF):

    tmpdir = tempfile.mkdtemp(prefix='cdetect_')

    factory = RawCX2NetworkFactory()
    parent_cx2 = factory.get_cx2network(interactome)

    pandas_cx2_factory = CX2NetworkPandasDataFrameFactory()
    df = pandas_cx2_factory.get_dataframe(parent_cx2)
    weight_col = next((col for col in df.columns if col.lower() == 'weight'), None)
    if weight_col is None:
        raise ValueError("No 'weight' column found (case-insensitive)")
    df = df.sort_values(weight_col, ascending=False)
    edgelist_files = []
    for cutoff in ppi_cutoffs:
        top_df = df.iloc[:int(len(df) * cutoff)+1]
        path = os.path.join(tmpdir, f'ppi_{cutoff}.id.edgelist.tsv')
        top_df[['source_id', 'target_id']].to_csv(path, sep='\t', index=False, header=False)
        edgelist_files.append(path)

    outputprefix = os.path.join(tmpdir, CDAPSHiDeFHierarchyGenerator.HIDEF_OUT_PREFIX)
    hier_generator = CDAPSHiDeFHierarchyGenerator()
    hier_generator._run_hidef(edgelist_files, outputprefix, algorithm, maxres, k)

    refiner = HiDeFHierarchyRefiner(ci_thre=containment_threshold,
                                    ji_thre=jaccard_threshold,
                                    min_term_size=min_system_size,
                                    min_diff=min_diff)

    refiner.refine_hierarchy(outprefix=outputprefix)

    cdaps_out_file = os.path.join(tmpdir,
                                  CDAPSHiDeFHierarchyGenerator.CDAPS_JSON_FILE)

    hier_generator = CDAPSHiDeFHierarchyGenerator()
    with open(cdaps_out_file, 'w') as out_stream:
        hier_generator.convert_hidef_output_to_cdaps(out_stream, tmpdir)

    cd = cdapsutil.CommunityDetection(runner=cdapsutil.ExternalResultsRunner())
    hierarchy = cd.run_community_detection(parent_cx2, algorithm=cdaps_out_file, uuid=ndex_uuid)

    return [hierarchy.to_cx2()]


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

        # Mute all logs except CRITICAL - Temporary fix - need to refactor cellmaps_generate_hierarchy
        # code to be more robust
        for logname in logging.root.manager.loggerDict:
            logging.getLogger(logname).setLevel(logging.CRITICAL)
        logging.getLogger().setLevel(logging.CRITICAL)

        if theargs.mode == 'networkfromembedding':
            result = [{'action': 'addNetworks',
                       'data': network_from_embedding_mode(embedding=theargs.embedding,
                                                           algorithm=theargs.similarity,
                                                           cutoff=theargs.embedding_cutoff,
                                                           )}]
        if theargs.mode == 'communitydetection':
            result = [{'action': 'addNetworks',
                       'data': community_detection_mode(interactome=theargs.input,
                                                        ndex_uuid=theargs.interactome_uuid,
                                                        ppi_cutoffs=theargs.ppi_cutoffs,
                                                        algorithm=theargs.hidef_algorithm,
                                                        maxres=theargs.maxres,
                                                        k=theargs.k,
                                                        containment_threshold=theargs.containment_threshold,
                                                        jaccard_threshold=theargs.jaccard_threshold,
                                                        min_system_size=theargs.min_system_size,
                                                        min_diff=theargs.min_diff)}]
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
