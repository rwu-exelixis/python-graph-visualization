from __future__ import annotations

from typing import Any, Optional

import pandas as pd
from pandas import DataFrame

from .node import Node
from .relationship import Relationship
from .visualization_graph import VisualizationGraph


def from_dfs(
    node_df: DataFrame, rel_df: DataFrame, node_radius_min_max: Optional[tuple[float, float]] = (3, 60)
) -> VisualizationGraph:
    """
    Create a VisualizationGraph from two pandas DataFrames.

    Parameters
    ----------
    node_df : DataFrame
        DataFrame containing node data.
    rel_df : DataFrame
        DataFrame containing relationship data.
    node_radius_min_max : tuple[float, float], optional
        Minimum and maximum node radius.
        To avoid tiny or huge nodes in the visualization, the node sizes are scaled to fit in the given range.
    """
    if node_radius_min_max and "size" in node_df.columns:
        node_df["size"] = _scale_node_size(
            node_df["size"], min_size=node_radius_min_max[0], max_size=node_radius_min_max[1]
        )

    nodes = []
    for _, row in node_df.iterrows():
        node = Node(**row.to_dict())
        nodes.append(node)

    relationships = []
    for _, row in rel_df.iterrows():
        rel = Relationship(**row.to_dict())
        relationships.append(rel)

    return VisualizationGraph(nodes=nodes, relationships=relationships)


def _scale_node_size(sizes: pd.Series[Any], min_size: float, max_size: float) -> pd.Series[Any]:
    normalized_sizes: pd.Series[Any] = (sizes - sizes.min()) / (sizes.max() - sizes.min())

    new_size_range = max_size - min_size

    range_scaled_sizes = normalized_sizes * new_size_range
    scaled_sizes = range_scaled_sizes + min_size

    return scaled_sizes
