from __future__ import annotations

from typing import Optional, Union

import neo4j.graph
from neo4j import Result
from pydantic import BaseModel, ValidationError

from neo4j_viz.node import Node
from neo4j_viz.relationship import Relationship
from neo4j_viz.visualization_graph import VisualizationGraph


def _parse_validation_error(e: ValidationError, entity_type: type[BaseModel]) -> None:
    for err in e.errors():
        loc = err["loc"][0]
        raise ValueError(
            f"Error for {entity_type.__name__.lower()} property '{loc}' with provided input '{err['input']}'. Reason: {err['msg']}"
        )


def from_neo4j(
    result: Union[neo4j.graph.Graph, Result],
    size_property: Optional[str] = None,
    node_caption: Optional[str] = "labels",
    relationship_caption: Optional[str] = "type",
    node_radius_min_max: Optional[tuple[float, float]] = (3, 60),
) -> VisualizationGraph:
    """
    Create a VisualizationGraph from a Neo4j Graph or Neo4j Result object.

    All node and relationship properties will be included in the visualization graph.
    If the properties are named as the fields of the `Node` or `Relationship` classes, they will be included as
    top level fields of the respective objects. Otherwise, they will be included in the `properties` dictionary.
    Additionally, a "labels" property will be added for nodes and a "type" property for relationships.

    Parameters
    ----------
    result : Union[neo4j.graph.Graph, Result]
        Query result either in shape of a Graph or result.
    size_property : str, optional
        Property to use for node size, by default None.
    node_caption : str, optional
        Property to use as the node caption, by default the node labels will be used.
    relationship_caption : str, optional
        Property to use as the relationship caption, by default the relationship type will be used.
    node_radius_min_max : tuple[float, float], optional
        Minimum and maximum node radius, by default (3, 60).
        To avoid tiny or huge nodes in the visualization, the node sizes are scaled to fit in the given range.
    """

    if isinstance(result, Result):
        graph = result.graph()
    elif isinstance(result, neo4j.graph.Graph):
        graph = result
    else:
        raise ValueError(f"Invalid input type `{type(result)}`. Expected `neo4j.Graph` or `neo4j.Result`")

    all_node_field_aliases = Node.all_validation_aliases()
    all_rel_field_aliases = Relationship.all_validation_aliases()

    try:
        nodes = [
            _map_node(node, all_node_field_aliases, size_property, caption_property=node_caption)
            for node in graph.nodes
        ]
    except ValueError as e:
        err_msg = str(e)
        if ("'size'" in err_msg) and (size_property is not None):
            err_msg = err_msg.replace("'size'", f"'{size_property}'")
        elif ("'caption'" in err_msg) and (node_caption is not None):
            err_msg = err_msg.replace("'caption'", f"'{node_caption}'")
        raise ValueError(err_msg)

    relationships = []
    try:
        for rel in graph.relationships:
            mapped_rel = _map_relationship(rel, all_rel_field_aliases, caption_property=relationship_caption)
            if mapped_rel:
                relationships.append(mapped_rel)
    except ValueError as e:
        err_msg = str(e)
        if ("'caption'" in err_msg) and (relationship_caption is not None):
            err_msg = err_msg.replace("'caption'", f"'{relationship_caption}'")
        raise ValueError(err_msg)

    VG = VisualizationGraph(nodes, relationships)

    if (node_radius_min_max is not None) and (size_property is not None):
        VG.resize_nodes(node_radius_min_max=node_radius_min_max)

    return VG


def _map_node(
    node: neo4j.graph.Node,
    all_node_field_aliases: set[str],
    size_property: Optional[str],
    caption_property: Optional[str],
) -> Node:
    top_level_fields = {"id": node.element_id}

    if size_property:
        top_level_fields["size"] = node.get(size_property)

    labels = sorted([label for label in node.labels])
    if caption_property:
        if caption_property == "labels":
            if len(labels) > 0:
                top_level_fields["caption"] = ":".join([label for label in labels])
        else:
            top_level_fields["caption"] = str(node.get(caption_property))

    properties = {}
    for prop, value in node.items():
        if prop not in all_node_field_aliases:
            properties[prop] = value
            continue

        if prop in top_level_fields:
            properties[prop] = value
            continue

        top_level_fields[prop] = value

    if "labels" in properties:
        properties["__labels"] = properties["labels"]
    properties["labels"] = labels

    try:
        viz_node = Node(**top_level_fields, properties=properties)
    except ValidationError as e:
        _parse_validation_error(e, Node)

    return viz_node


def _map_relationship(
    rel: neo4j.graph.Relationship, all_rel_field_aliases: set[str], caption_property: Optional[str]
) -> Optional[Relationship]:
    if rel.start_node is None or rel.end_node is None:
        return None

    top_level_fields = {"id": rel.element_id, "source": rel.start_node.element_id, "target": rel.end_node.element_id}

    if caption_property:
        if caption_property == "type":
            top_level_fields["caption"] = rel.type
        else:
            top_level_fields["caption"] = str(rel.get(caption_property))

    properties = {}
    for prop, value in rel.items():
        if prop not in all_rel_field_aliases:
            properties[prop] = value
            continue

        if prop in top_level_fields:
            properties[prop] = value
            continue

        top_level_fields[prop] = value

    if "type" in properties:
        properties["__type"] = properties["type"]
    properties["type"] = rel.type

    try:
        viz_rel = Relationship(**top_level_fields, properties=properties)
    except ValidationError as e:
        _parse_validation_error(e, Relationship)

    return viz_rel
