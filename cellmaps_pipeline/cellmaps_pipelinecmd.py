#! /usr/bin/env python

import argparse
import sys
import logging
import logging.config
import json

from cellmaps_utils import logutils
from cellmaps_utils import constants
from cellmaps_imagedownloader.runner import CellmapsImageDownloader
from cellmaps_ppidownloader.runner import CellmapsPPIDownloader
from cellmaps_pipeline.runner import ProgrammaticPipelineRunner
import cellmaps_pipeline
from cellmaps_pipeline.runner import CellmapsPipeline

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
    parser.add_argument('outdir', help='Output directory')
    parser.add_argument('--samples',
                        help='CSV file with list of IF images to download '
                             'in format of filename,if_plate_id,position,'
                             'sample,status,locations,antibody,ensembl_ids,'
                             'gene_names\n/archive/1/1_A1_1_,1,A1,1,35,'
                             'Golgi apparatus,HPA000992,ENSG00000066455,GOLGA5')
    parser.add_argument('--unique',
                        help='CSV file of unique samples '
                             'in format of:\n'
                             'antibody,ensembl_ids,gene_names,atlas_name,'
                             'locations,n_location\n'
                             'HPA040086,ENSG00000094914,AAAS,U-2 OS,'
                             'Nuclear membrane,1')
    parser.add_argument('--edgelist',
                        help='edgelist TSV file in format of:\n'
                             'GeneID1\tSymbol1\tGeneID2\tSymbol2\n'
                             '10159\tATP6AP2\t2\tA2M')
    parser.add_argument('--baitlist',
                        help='baitlist TSV file in format of:\n'
                             'GeneSymbol\tGeneID\t# Interactors\n'
                             '"ADA"\t"100"\t1.')
    parser.add_argument('--model_path', type=str,
                        help='Path to model file. A model file to download '
                             'is here: '
                             'https://github.com/'
                             'CellProfiling/densenet/releases/download/'
                             'v0.1.0/external_crop512_focal_slov_hardlog'
                             '_class_densenet121_dropout_i768_aug2_5folds'
                             '_fold0_final.pth')
    parser.add_argument('--fold', default=1, type=int, help='Image node attribute file fold to use')
    parser.add_argument('--proteinatlasxml',
                        default='https://www.proteinatlas.org/download/proteinatlas.xml.gz',
                        help='URL or path to proteinatlas.xml or proteinatlas.xml.gz file '
                             'used to look for images not found in the standard location '
                             'on HPA')
    parser.add_argument('--ppi_cutoffs', nargs='+', type=float,
                        default=[0.001, 0.002, 0.003, 0.004, 0.005, 0.006,
                                 0.007, 0.008, 0.009, 0.01, 0.02, 0.03,
                                 0.04, 0.05, 0.10],
                        help='Cutoffs used to generate PPI input networks. For example, '
                             'a value of 0.1 means to generate PPI input network using the '
                             'top ten percent of coembedding entries. Each cutoff generates '
                             'another PPI network')
    parser.add_argument('--provenance',
                        help='Path to file containing provenance '
                             'information about input files in JSON format. '
                             'This is required and not including will output '
                             'and error message with example of file')
    parser.add_argument('--fake', action='store_true',
                        help='If set, generate fake data for every step')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat '
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module. Messages are '
                             'output at these python logging levels '
                             '-v = ERROR, -vv = WARNING, -vvv = INFO, '
                             '-vvvv = DEBUG, -vvvvv = NOTSET (default no '
                             'logging)')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 cellmaps_pipeline.__version__))

    return parser.parse_args(args)


def main(args):
    """
    Main entry point for program

    :param args: arguments passed to command line usually :py:func:`sys.argv[1:]`
    :type args: list

    :return: return value of :py:meth:`cellmaps_pipeline.runner.CellmapsPipeline.run`
             or ``2`` if an exception is raised
    :rtype: int
    """
    withguid = CellmapsPPIDownloader.get_example_provenance(with_ids=True)
    withguid.update(CellmapsImageDownloader.get_example_provenance(with_ids=True))

    register = CellmapsPPIDownloader.get_example_provenance()
    register.update(CellmapsImageDownloader.get_example_provenance())

    withguids_json = json.dumps(withguid, indent=2)
    register_json = json.dumps(register, indent=2)

    desc = """
Version {version}

Runs the full cellmaps pipeline

In addition, the --provenance flag is required and must be set to a path 
to a JSON file. 

If datasets are already registered with FAIRSCAPE then the following is sufficient:

{withguids}

If datasets are NOT registered, then the following is required:

{register}

Additional optional fields for registering datasets include 
'url', 'used-by', 'associated-publication', and 'additional-documentation'
    """.format(version=cellmaps_pipeline.__version__,
               withguids=withguids_json,
               register=register_json)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = cellmaps_pipeline.__version__

    try:
        logutils.setup_cmd_logging(theargs)

        if theargs.provenance is None:
            sys.stderr.write('\n\n--provenance flag is required to run this tool. '
                             'Please pass '
                             'a path to a JSON file with the following data:\n\n')
            sys.stderr.write('If datasets are already registered with '
                             'FAIRSCAPE then the following is sufficient:\n\n')
            sys.stderr.write(withguids_json + '\n\n')
            sys.stderr.write('If datasets are NOT registered, then the following is required:\n\n')
            sys.stderr.write(register_json + '\n\n')
            return 1

        # load the provenance as a dict
        with open(theargs.provenance, 'r') as f:
            json_prov = json.load(f)

        runner = ProgrammaticPipelineRunner(outdir=theargs.outdir,
                                            samples=theargs.samples,
                                            unique=theargs.unique,
                                            edgelist=theargs.edgelist,
                                            baitlist=theargs.baitlist,
                                            model_path=theargs.model_path,
                                            proteinatlasxml=theargs.proteinatlasxml,
                                            ppi_cutoffs=theargs.ppi_cutoffs,
                                            fake=theargs.fake,
                                            provenance=json_prov,
                                            fold=theargs.fold,
                                            input_data_dict=theargs.__dict__)

        return CellmapsPipeline(outdir=theargs.outdir,
                                runner=runner,
                                input_data_dict=theargs.__dict__).run()
    except Exception as e:
        logger.exception('Caught exception: ' + str(e))
        return 2
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
