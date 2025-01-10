import pytest

from neo4j_viz import Node, VisualizationGraph
from neo4j_viz.node import NodeIdType, NodeSizeType


def test_resize_nodes() -> None:
    nodes = [
        Node(id=42),
        Node(id="1337", size=10),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    new_sizes: dict[NodeIdType, NodeSizeType] = {"1337": 20}
    VG.resize_nodes(new_sizes)

    assert VG.nodes[0].size is None
    assert VG.nodes[1].size == 20

    new_sizes = {42: 8.1, "1337": 3}
    VG.resize_nodes(new_sizes)

    assert VG.nodes[0].size == 8.1
    assert VG.nodes[1].size == 3

    new_sizes = {42: -4.2}
    with pytest.raises(ValueError, match="Size for node '42' must be non-negative, but was -4.2"):
        VG.resize_nodes(new_sizes)
