from __future__ import annotations

from dataclasses import asdict, dataclass
from json import dumps
from typing import Any, Optional

from .options import CaptionAlignment


@dataclass(frozen=True, repr=True)
class Node:
    """
    A node in a graph to visualize.
    Hold options availble in the NVL library (see https://neo4j.com/docs/nvl/current/base-library/#_nodes)

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
    size: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        # skip None values in the dict
        return {k:v for k, v in asdict(self).items() if v is not None}

    def to_json(self) -> str:
        return dumps(self.to_dict())
