from __future__ import annotations

from typing import Any, Optional, Union

from IPython.display import HTML
from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color

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

    def color_nodes(self, property: str, colors: dict[Any, Union[Color, str]], override: bool = False) -> None:
        for node in self.nodes:
            color = colors.get(getattr(node, property))

            if color is None:
                continue

            if node.color is not None and not override:
                continue

            if isinstance(color, str):
                node.color = Color(color)
            else:
                node.color = color
