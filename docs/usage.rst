=====
Usage
=====

This page should provide information on how to use cellmaps_pipeline

In a project
--------------

To use Cell Maps Pipeline in a project:

.. code-block:: python

    import os
    import json
    from cellmaps_pipeline.runner import ProgrammaticPipelineRunner
    from cellmaps_pipeline.runner import CellmapsPipeline

    # load the provenance as a dict
        with open(os.path.join('examples', 'provenance.json'), 'r') as f:
            json_prov = json.load(f)

    runner = ProgrammaticPipelineRunner(outdir='testrun',
                                        samples=os.path.join('examples', 'samples.csv'),
                                        unique=os.path.join('examples', 'unique.csv'),
                                        edgelist=os.path.join('examples', 'edgelist.tsv'),
                                        baitlist=os.path.join('examples', 'baitlist.tsv'),
                                        model_path='https://github.com/CellProfiling/densenet/releases/download/v0.1.0/external_crop512_focal_slov_hardlog_class_densenet121_dropout_i768_aug2_5folds_fold0_final.pth',
                                        provenance=json_prov,
                                        ppi_cutoffs=[0.001, 0.01],
                                        input_data_dict={})

    pipeline = CellmapsPipeline(outdir='testrun',
                                runner=runner,
                                input_data_dict={})
    print('Status code: ' + str(pipeline.run()))


On the command line
---------------------

For information invoke :code:`cellmaps_pipelinecmd.py -h`

**Example usage for CM4AI data**

Coming soon...

**Example usage**

The cell maps pipeline requires the following input files for building MuSIC maps by integrating IF images with an AP-MS interaction network: 

1) samples file: CSV file with list of IF images to download (see sample samples file in examples folder)
2) unique file: CSV file of unique samples (see sample unique file in examples folder)
3) bait list file: TSV file of baits used for AP-MS experiments
4) edge list file: TSV file of edges for protein interaction network
5) provenance: file containing provenance information about input files in JSON format (see sample provenance file in examples folder)

.. code-block::

   cellmaps_pipelinecmd.py ./cellmaps_pipeline_outdir --samples examples/samples.csv --unique examples/unique.csv \
                           --baitlist examples/baitlist.tsv --edgelist examples/edgelist.tsv \
                           --provenance examples/provenance.json
