from typing import Generator

import pytest
from neo4j import Session

from neo4j_viz.neo4j import from_neo4j
from neo4j_viz.node import Node


@pytest.fixture(scope="class", autouse=True)
def graph_setup(neo4j_session: Session) -> Generator[None, None, None]:
    neo4j_session.run(
        "CREATE (a:_CI_A {name:'Alice', height:20})-[:KNOWS {year: 2025}]->(b:_CI_A:_CI_B {name:'Bob', height:10}), (b)-[:RELATED {year: 2015}]->(a)"
    )
    yield
    neo4j_session.run("MATCH (n:_CI_A|_CI_B) DETACH DELETE n")


@pytest.mark.requires_neo4j_and_gds
def test_from_neo4j_graph(neo4j_session: Session) -> None:
    graph = neo4j_session.run("MATCH (a:_CI_A|_CI_B)-[r]->(b) RETURN a, b, r ORDER BY a").graph()

    VG = from_neo4j(graph)

    node_ids: list[str] = [node.element_id for node in graph.nodes]

    expected_nodes = [
        Node(id=node_ids[0], caption="_CI_A", labels=["_CI_A"], name="Alice", height=20),
        Node(id=node_ids[1], caption="_CI_A:_CI_B", labels=["_CI_A", "_CI_B"], name="Bob", height=10),
    ]

    assert len(VG.nodes) == 2
    assert sorted(VG.nodes, key=lambda x: x.name) == expected_nodes  # type: ignore[attr-defined]

    assert len(VG.relationships) == 2
    vg_rels = sorted([(e.source, e.target, e.caption) for e in VG.relationships], key=lambda x: x[2] if x[2] else "foo")
    assert vg_rels == [
        (node_ids[0], node_ids[1], "KNOWS"),
        (node_ids[1], node_ids[0], "RELATED"),
    ]


@pytest.mark.requires_neo4j_and_gds
def test_from_neo4j_result(neo4j_session: Session) -> None:
    result = neo4j_session.run("MATCH (a:_CI_A|_CI_B)-[r]->(b) RETURN a, b, r ORDER BY a")

    VG = from_neo4j(result)

    graph = result.graph()
    node_ids: list[str] = [node.element_id for node in graph.nodes]

    expected_nodes = [
        Node(id=node_ids[0], caption="_CI_A", labels=["_CI_A"], name="Alice", height=20),
        Node(id=node_ids[1], caption="_CI_A:_CI_B", labels=["_CI_A", "_CI_B"], name="Bob", height=10),
    ]

    assert len(VG.nodes) == 2
    assert sorted(VG.nodes, key=lambda x: x.name) == expected_nodes  # type: ignore[attr-defined]

    assert len(VG.relationships) == 2
    vg_rels = sorted([(e.source, e.target, e.caption) for e in VG.relationships], key=lambda x: x[2] if x[2] else "foo")
    assert vg_rels == [
        (node_ids[0], node_ids[1], "KNOWS"),
        (node_ids[1], node_ids[0], "RELATED"),
    ]


@pytest.mark.requires_neo4j_and_gds
def test_from_neo4j_graph_full(neo4j_session: Session) -> None:
    graph = neo4j_session.run("MATCH (a:_CI_A|_CI_B)-[r]->(b) RETURN a, b, r ORDER BY a").graph()

    VG = from_neo4j(graph, node_caption="name", relationship_caption="year", size_property="height")

    node_ids: list[str] = [node.element_id for node in graph.nodes]

    expected_nodes = [
        Node(id=node_ids[0], caption="Alice", labels=["_CI_A"], name="Alice", height=20, size=60.0),
        Node(id=node_ids[1], caption="Bob", labels=["_CI_A", "_CI_B"], name="Bob", height=10, size=3.0),
    ]

    assert len(VG.nodes) == 2
    assert sorted(VG.nodes, key=lambda x: x.name) == expected_nodes  # type: ignore[attr-defined]

    assert len(VG.relationships) == 2
    vg_rels = sorted([(e.source, e.target, e.caption) for e in VG.relationships], key=lambda x: x[2] if x[2] else "foo")
    assert vg_rels == [
        (node_ids[1], node_ids[0], "2015"),
        (node_ids[0], node_ids[1], "2025"),
    ]
