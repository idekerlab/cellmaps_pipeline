import json

import pytest
import pandas as pd
import numpy as np
import tempfile
import os

from cellmaps_pipeline.cellmaps_cywebserviceapp import network_from_embedding_mode, community_detection_mode
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

def _create_dummy_cx2_network(path):
    net = CX2Network()
    nodes = [net.add_node(attributes={'name': chr(65+i)}) for i in range(10)]
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            net.add_edge(source=nodes[i], target=nodes[j], attributes={'weight': 0.9})

    with open(path, 'w') as f:
        json.dump(net.to_cx2(), f)

def test_community_detection_mode_runs_and_returns_cx2():
    with tempfile.TemporaryDirectory() as tempdir:
        cx2_path = os.path.join(tempdir, 'dummy.cx2')
        _create_dummy_cx2_network(cx2_path)

        result = community_detection_mode(
            interactome=cx2_path,
            ndex_uuid='test-uuid-123'
        )

        assert isinstance(result, list)
        assert len(result) == 1

        factory = RawCX2NetworkFactory()
        net = factory.get_cx2network(result[0])
        assert isinstance(net, CX2Network)
        assert len(net.get_nodes()) > 0
