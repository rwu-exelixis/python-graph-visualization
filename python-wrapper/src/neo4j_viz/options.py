from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class CaptionAlignment(str, Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class RenderOptions(BaseModel, extra="allow"):
    """
    Options as documented at https://neo4j.com/docs/nvl/current/base-library/#_options
    """

    layout: Optional[RenderOptions.Layout] = None
    renderer: Optional[Renderer] = None

    pan_X: Optional[float] = Field(None, serialization_alias="panX")
    pan_Y: Optional[float] = Field(None, serialization_alias="panY")

    initial_zoom: Optional[float] = Field(None, serialization_alias="initialZoom", description="The initial zoom level")
    max_zoom: Optional[float] = Field(10, serialization_alias="maxZoom", description="The maximum zoom level allowed.")
    min_zoom: Optional[float] = Field(
        0.075, serialization_alias="minZoom", description="The minimum zoom level allowed"
    )
    allow_dynamic_min_zoom: Optional[bool] = Field(None, serialization_alias="allowDynamicMinZoom")

    class Layout(str, Enum):
        FORCE_DIRECTED = "forcedirected"
        HIERARCHICAL = "hierarchical"
        GRID = "grid"
        # TODO expose free layout for X,Y based

    class Renderer(str, Enum):
        WEB_GL = "webgl"
        CANVAS = "canvas"

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)
