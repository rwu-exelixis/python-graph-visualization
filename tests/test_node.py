from neo4j_viz import CaptionAlignment, Node


def test_nodes_with_all_options() -> None:
    node = Node(
        id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
        caption="Person",
        captionAlign=CaptionAlignment.TOP,
        captionSize=12,
        color="#FF0000",
        size=10,
    )

    assert node.model_dump() == {
        "id": "4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
        "caption": "Person",
        "captionAlign": "top",
        "captionSize": 12,
        "color": "#FF0000",
        "size": 10,
    }


def test_nodes_minimal_node() -> None:
    node = Node(
        id="1",
    )

    # TODO is this okay for NVL? (omit would be less data)
    assert node.to_dict() == {
        "id": "1",
    }
