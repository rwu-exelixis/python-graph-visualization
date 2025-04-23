from __future__ import annotations

from typing import Any

from pydantic import BaseModel, model_validator
from pydantic.alias_generators import to_snake


class CaseInsensitiveModel(BaseModel):
    @model_validator(mode="before")
    def _make_fields_snake(cls, values: Any) -> Any:
        return {to_snake(k): v for k, v in values.items()}
