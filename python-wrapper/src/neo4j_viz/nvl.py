from __future__ import annotations

import json
import uuid
from importlib.resources import files
from typing import Optional

from IPython.display import HTML

from .node import Node
from .options import RenderOptions
from .relationship import Relationship


class NVL:
    def __init__(self) -> None:
        # at which point we get None?
        base_folder = files("neo4j_viz")
        resource_folder = base_folder / "resources"
        nvl_entry_point = resource_folder / "nvl_entrypoint"

        js_path = nvl_entry_point / "base.js"

        with js_path.open("r", encoding="utf-8") as file:
            self.library_code = file.read()

    def render(
        self,
        nodes: list[Node],
        relationships: list[Relationship],
        # TODO combine with width and height?
        options: Optional[RenderOptions] = None,
        width: str = "100%",
        height: str = "300px",
    ) -> HTML:
        nodes_json = json.dumps([node.to_dict() for node in nodes])
        rels_json = json.dumps([rel.to_dict() for rel in relationships])

        render_options_json = json.dumps(options.to_dict()) if options is not None else {}

        container_id = str(uuid.uuid4())
        js_code = f"""
        var myNvl = new NVLBase.NVL(
            document.getElementById('{container_id}'),
            {nodes_json},
            {rels_json},
            {render_options_json}
        );
        """
        full_code = self.library_code + js_code
        html_output = f"""
        <div id="{container_id}" style="width: {width}; height: {height};"></div>
        <script>
            {full_code}
        </script>
        """
        return HTML(html_output)  # type: ignore[no-untyped-call]
