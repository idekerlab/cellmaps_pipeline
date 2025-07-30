import pytest
import pandas as pd
import numpy as np
import tempfile
import os

from cellmaps_pipeline.cellmaps_cywebserviceapp import network_from_embedding_mode
from ndex2.cx2 import CX2Network, RawCX2NetworkFactory


def _write_dummy_embedding(file_path):
    df = pd.DataFrame({
        'x': [0.1, 0.2, 0.3],
        'y': [0.4, 0.5, 0.6],
        'z': [0.7, 0.8, 0.9]
    }, index=['A', 'B', 'C'])
    df.to_csv(file_path, sep='\t')

def test_network_from_embedding_mode_creates_network():
    with tempfile.TemporaryDirectory() as tempdir:
        embedding_file = os.path.join(tempdir, 'embedding.tsv')
        _write_dummy_embedding(embedding_file)

        cx2list = network_from_embedding_mode(embedding=embedding_file,
                                              algorithm='cosine',
                                              cutoff=0.5)
        assert isinstance(cx2list, list)
        assert len(cx2list) == 1

        factory = RawCX2NetworkFactory()
        net = factory.get_cx2network(cx2list[0])

        assert 'name' in net.get_network_attributes().keys()
        assert 'description' in net.get_network_attributes().keys()
        assert len(net.get_nodes()) == 3
        assert len(net.get_edges()) > 0
