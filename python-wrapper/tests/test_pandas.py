from pandas import DataFrame
from pydantic_extra_types.color import Color

from neo4j_viz.pandas import from_dfs


def test_from_df() -> None:
    nodes = DataFrame(
        {"id": [0, 1], "caption": ["A", "B"], "size": [1337, 42], "color": "#FF0000", "instrument": ["piano", "guitar"]}
    )
    relationships = DataFrame(
        {
            "source": [0, 1],
            "target": [1, 0],
            "caption": ["REL", "REL2"],
            "weight": [1.0, 2.0],
        }
    )
    VG = from_dfs(nodes, relationships, node_radius_min_max=(42, 1337))

    assert len(VG.nodes) == 2

    assert VG.nodes[0].id == 0
    assert VG.nodes[0].caption == "A"
    assert VG.nodes[0].size == 1337
    assert VG.nodes[0].color == Color("#ff0000")
    assert VG.nodes[0].properties == {"instrument": "piano"}

    assert VG.nodes[1].id == 1
    assert VG.nodes[1].caption == "B"
    assert VG.nodes[1].size == 42
    assert VG.nodes[1].color == Color("#ff0000")
    assert VG.nodes[1].properties == {"instrument": "guitar"}

    assert len(VG.relationships) == 2

    assert VG.relationships[0].source == 0
    assert VG.relationships[0].target == 1
    assert VG.relationships[0].caption == "REL"
    assert VG.relationships[0].properties == {"weight": 1.0}

    assert VG.relationships[1].source == 1
    assert VG.relationships[1].target == 0
    assert VG.relationships[1].caption == "REL2"
    assert VG.relationships[1].properties == {"weight": 2.0}


def test_from_dfs() -> None:
    nodes = [
        DataFrame(
            {
                "id": [0],
                "caption": ["A"],
                "size": [1337],
                "color": "#FF0000",
            }
        ),
        DataFrame(
            {
                "id": [1],
                "caption": ["B"],
                "size": [42],
                "color": "#FF0000",
            }
        ),
    ]

    relationships = [
        DataFrame(
            {
                "source": [0],
                "target": [1],
                "caption": ["REL"],
            }
        ),
        DataFrame(
            {
                "source": [1],
                "target": [0],
                "caption": ["REL2"],
            }
        ),
    ]
    VG = from_dfs(nodes, relationships, node_radius_min_max=(42, 1337))

    assert len(VG.nodes) == 2

    assert VG.nodes[0].id == 0
    assert VG.nodes[0].caption == "A"
    assert VG.nodes[0].size == 1337
    assert VG.nodes[0].color == Color("#ff0000")

    assert VG.nodes[1].id == 1
    assert VG.nodes[1].caption == "B"
    assert VG.nodes[1].size == 42
    assert VG.nodes[0].color == Color("#ff0000")

    assert len(VG.relationships) == 2

    assert VG.relationships[0].source == 0
    assert VG.relationships[0].target == 1
    assert VG.relationships[0].caption == "REL"

    assert VG.relationships[1].source == 1
    assert VG.relationships[1].target == 0
    assert VG.relationships[1].caption == "REL2"
