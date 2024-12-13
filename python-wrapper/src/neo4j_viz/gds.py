from __future__ import annotations

from itertools import chain
from typing import Callable, Optional
import warnings

import pandas as pd
from graphdatascience import Graph, GraphDataScience

from .pandas import from_dfs
from .visualization_graph import VisualizationGraph


def _node_dfs(
    gds: GraphDataScience, G: Graph, node_properties: list[str], node_labels: list[str]
) -> dict[str, pd.DataFrame]:
    return {
        lbl: gds.graph.nodeProperties.stream(
            G, node_properties=node_properties, node_labels=[lbl], separate_property_columns=True
        )
        for lbl in node_labels
    }


def _rel_df(gds: GraphDataScience, G: Graph) -> pd.DataFrame:
    return gds.graph.relationships.stream(G)


def from_gds(
    gds: GraphDataScience,
    G: Graph,
    size_property: Optional[str] = None,
    additional_node_properties: Optional[list[str]] = None,
    node_radius_min_max: Optional[tuple[float, float]] = (3, 60),
) -> VisualizationGraph:
    node_properties_from_gds = G.node_properties()
    assert isinstance(node_properties_from_gds, pd.Series)
    actual_node_properties = list(chain.from_iterable(node_properties_from_gds.to_dict().values()))

    if size_property is not None and size_property not in actual_node_properties:
        raise ValueError(f"There is no node property '{size_property}' in graph '{G.name()}'")

    if additional_node_properties is not None:
        for prop in additional_node_properties:
            if prop not in actual_node_properties:
                raise ValueError(f"There is no node property '{prop}' in graph '{G.name()}'")

    node_properties = set()
    if additional_node_properties is not None:
        node_properties.update(additional_node_properties)

    if size_property is not None:
        node_properties.add(size_property)

    node_properties = list(node_properties)
    node_dfs = _node_dfs(gds, G, node_properties, G.node_labels())
    for df in node_dfs.values():
        df.rename(columns={"nodeId": "id"}, inplace=True)

    node_props_df = pd.concat(node_dfs.values(), ignore_index=True, axis=0).drop_duplicates()
    if size_property is not None:
        node_props_df.rename(columns={size_property: "size"}, inplace=True)

    for lbl, df in node_dfs.items():
        df["labels"] = lbl

    node_lbls_df = pd.concat([df[["id", "labels"]] for df in node_dfs.values()], ignore_index=True, axis=0)
    node_lbls_df = node_lbls_df.groupby("id").agg({"labels": list})

    node_df = node_props_df.merge(node_lbls_df, on="id")

    if node_radius_min_max and size_property:
        min_radius, max_radius = node_radius_min_max
        max_size = node_df["size"].max()
        node_df["size"] = node_df["size"]*max_radius/max_size
        if node_df["size"].min() < min_radius:
            warnings.warn("Some nodes have a size smaller than the minimum radius.")

    rel_df = _rel_df(gds, G)
    rel_df.rename(columns={"sourceNodeId": "source", "targetNodeId": "target"}, inplace=True)

    return from_dfs(node_df, rel_df)
