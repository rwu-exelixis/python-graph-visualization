import pytest
from pydantic_extra_types.color import Color

from neo4j_viz import Node, VisualizationGraph
from neo4j_viz.colors import NEO4J_COLORS_CONTINUOUS, NEO4J_COLORS_DISCRETE, PropertyType


@pytest.mark.parametrize("override", [True, False])
def test_color_nodes_dict(override: bool) -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", color="#FF0000"),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption", {"Person": "#000000", "Product": "#00FF00"}, override=override)

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    if override:
        assert VG.nodes[2].color == Color("#00ff00")
    else:
        assert VG.nodes[2].color == Color("#ff0000")


@pytest.mark.parametrize("override", [True, False])
def test_color_nodes_iter_basic(override: bool) -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", color="#FF0000"),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption", ["#000000", "#00FF00"], override=override)

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    if override:
        assert VG.nodes[2].color == Color("#00ff00")
    else:
        assert VG.nodes[2].color == Color("#ff0000")


def test_color_nodes_iter_exhausted() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Review"),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    with pytest.warns(
        UserWarning,
        match=(
            "Ran out of colors for property 'caption'. 3 colors were needed, but only 2 were given, so reused colors"
        ),
    ):
        VG.color_nodes("caption", ["#000000", "#00FF00"])

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    assert VG.nodes[2].color == Color("#00ff00")
    assert VG.nodes[3].color == Color("#000000")


@pytest.mark.filterwarnings("ignore:pkg_resources is deprecated as an API")
def test_color_nodes_palette() -> None:
    from palettable.wesanderson import Moonrise1_5  # type: ignore[import-untyped]

    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Review"),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption", Moonrise1_5.colors)

    assert VG.nodes[0].color == Color((114, 202, 221))
    assert VG.nodes[1].color == Color((240, 165, 176))
    assert VG.nodes[2].color == Color((240, 165, 176))
    assert VG.nodes[3].color == Color((140, 133, 54))


def test_color_nodes_default() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product"),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:12", caption="Review"),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("caption")

    assert VG.nodes[0].color == Color(NEO4J_COLORS_DISCRETE[0])
    assert VG.nodes[1].color == Color(NEO4J_COLORS_DISCRETE[1])
    assert VG.nodes[2].color == Color(NEO4J_COLORS_DISCRETE[1])
    assert VG.nodes[3].color == Color(NEO4J_COLORS_DISCRETE[2])


def test_color_nodes_continuous_default() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", rank=10),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", rank=20),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", rank=30),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("rank", property_type=PropertyType.CONTINUOUS)

    assert VG.nodes[0].color == Color(NEO4J_COLORS_CONTINUOUS[0])
    assert VG.nodes[1].color == Color(NEO4J_COLORS_CONTINUOUS[128])
    assert VG.nodes[2].color == Color(NEO4J_COLORS_CONTINUOUS[255])


def test_color_nodes_continuous_custom() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", rank=10),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", rank=18),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", rank=30),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    colors = [(0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255)]
    VG.color_nodes("rank", colors=colors, property_type=PropertyType.CONTINUOUS)

    assert VG.nodes[0].color == Color("black")
    assert VG.nodes[1].color == Color((85, 85, 85))
    assert VG.nodes[2].color == Color("white")


def test_color_nodes_continuous_forbidden() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", rank=10),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", rank=30),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    with pytest.raises(
        ValueError, match="For continuous properties, `colors` must be a list of colors representing a range"
    ):
        VG.color_nodes("rank", {10: "#000000", 30: "#00FF00"}, property_type=PropertyType.CONTINUOUS)  # type: ignore[arg-type]


def test_color_nodes_lists() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person", labels=["Person"]),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product", labels=["Product"]),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", labels=["Product"]),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:1", caption="Both", labels=["Person", "Product"]),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:2", caption="Both again", labels=["Person", "Product"]),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:3", caption="Both reorder", labels=["Product", "Person"]),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("labels", ["#000000", "#00FF00", "#FF0000", "#0000FF"])

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    assert VG.nodes[2].color == Color("#00ff00")
    assert VG.nodes[3].color == Color("#ff0000")
    assert VG.nodes[4].color == Color("#ff0000")
    assert VG.nodes[5].color == Color("#0000ff")


def test_color_nodes_sets() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person", labels={"Person"}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product", labels={"Product"}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", labels={"Product"}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:1", caption="Both", labels={"Person", "Product"}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:2", caption="Both again", labels={"Person", "Product"}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:3", caption="Both reorder", labels={"Product", "Person"}),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("labels", ["#000000", "#00FF00", "#FF0000", "#0000FF"])

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    assert VG.nodes[2].color == Color("#00ff00")
    assert VG.nodes[3].color == Color("#ff0000")
    assert VG.nodes[4].color == Color("#ff0000")
    assert VG.nodes[4].color == Color("#ff0000")


def test_color_nodes_dicts() -> None:
    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person", config={"age": 18}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:6", caption="Product", config={"price": 100}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:11", caption="Product", config={"price": 100}),
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:1", caption="Product", config={"price": 1}),
    ]

    VG = VisualizationGraph(nodes=nodes, relationships=[])

    VG.color_nodes("config", ["#000000", "#00FF00", "#FF0000", "#0000FF"])

    assert VG.nodes[0].color == Color("#000000")
    assert VG.nodes[1].color == Color("#00ff00")
    assert VG.nodes[2].color == Color("#00ff00")
    assert VG.nodes[3].color == Color("#ff0000")


def test_color_nodes_unhashable() -> None:
    nodes = [
        Node(
            id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0",
            caption="Person",
            config={"movies": ["Star Wars", "Star Trek"]},
        ),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])

    with pytest.raises(ValueError, match="Unable to color nodes by unhashable property type '<class 'dict'>'"):
        VG.color_nodes("config", ["#000000"])

    nodes = [
        Node(id="4:d09f48a4-5fca-421d-921d-a30a896c604d:0", caption="Person", list_of_lists=[[1, 2], [3, 4]]),
    ]
    VG = VisualizationGraph(nodes=nodes, relationships=[])
    with pytest.raises(ValueError, match="Unable to color nodes by unhashable property type '<class 'list'>'"):
        VG.color_nodes("list_of_lists", ["#000000"])
