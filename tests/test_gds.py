import pytest
from graphdatascience import GraphDataScience
from pandas import DataFrame

from neo4j_viz import Node
from neo4j_viz.gds import from_gds


@pytest.mark.requires_neo4j_and_gds
def test_from_gds() -> None:
    nodes = DataFrame(
        {
            "nodeId": [0, 1, 2],
            "labels": ["A", "C", ["A", "B"]],
            "score": [1337, 42, 3.14],
            "component": [1, 4, 2],
        }
    )
    rels = DataFrame(
        {
            "sourceNodeId": [0, 1, 2],
            "targetNodeId": [1, 2, 0],
            "relationshipType": ["REL", "REL2", "REL"],
        }
    )

    gds = GraphDataScience("bolt://localhost:7687", auth=None)

    with gds.graph.construct("flo", nodes, rels) as G:
        VG = from_gds(gds, G, size_property="score", additional_node_properties=["component"])

        assert len(VG.nodes) == 3
        assert sorted(VG.nodes, key=lambda x: x.id) == [
            Node(id=0, labels=["A"], size=float(1337), component=float(1)),
            Node(id=1, labels=["C"], size=float(42), component=float(4)),
            Node(id=2, labels=["A", "B"], size=float(3.14), component=float(2)),
        ]

        assert len(VG.relationships) == 3
        vg_rels = sorted([(e.source, e.target, e.relationshipType) for e in VG.relationships], key=lambda x: x[0])  # type: ignore[attr-defined]
        assert vg_rels == [
            (0, 1, "REL"),
            (1, 2, "REL2"),
            (2, 0, "REL"),
        ]
