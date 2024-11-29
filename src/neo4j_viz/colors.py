from collections.abc import Iterable
from typing import Any, Union

from pydantic_extra_types.color import ColorType

ColorsType = Union[dict[Any, ColorType], Iterable[ColorType]]
