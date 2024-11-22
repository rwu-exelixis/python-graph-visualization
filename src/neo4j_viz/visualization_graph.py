from __future__ import annotations

from typing import Any, Optional

from IPython.display import HTML
from pydantic import BaseModel, Field

from .node import Node
from .nvl import NVL
from .relationship import Relationship


class VisualizationGraph(BaseModel):
    """
    A graph to visualize.
    """

    nodes: list[Node] = Field(description="The nodes in the graph")
    relationships: list[Relationship] = Field(description="The relationships in the graph")

    def render(self, options: Optional[dict[str, Any]] = None, width: str = "100%", height: str = "300px") -> HTML:
        return NVL().render(self.nodes, self.relationships, options=options, width=width, height=height)
