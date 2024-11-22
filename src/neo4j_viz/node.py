from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from .options import CaptionAlignment


class Node(BaseModel):
    """
    A node in a graph to visualize.
    Hold options available in the NVL library (see https://neo4j.com/docs/nvl/current/base-library/#_nodes)

    Args:
        id (str): Unique identifier for the node.
        captionAlign (Optional[CaptionAlignment]): The alignment of the caption text.
        captionSize (Optional[int]): The size of the caption text.
        color (Optional[str]): The color of the node. A hex color string.
        size (Optional[int]): The size of the node as radius in pixel.
    """

    id: str
    caption: Optional[str] = None
    captionAlign: Optional[CaptionAlignment] = None
    captionSize: Optional[int] = None
    color: Optional[str] = None
    size: Optional[int] = Field(None, ge=0)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)
