from __future__ import annotations

import json
import uuid
from importlib.resources import files

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

    def unsupported_field_type_error(self, e: TypeError, entity: str) -> Exception:
        if "not JSON serializable" in str(e):
            return ValueError(f"A field of a {entity} object is not supported: {str(e)}")
        return e

    def render(
        self,
        nodes: list[Node],
        relationships: list[Relationship],
        render_options: RenderOptions,
        width: str,
        height: str,
    ) -> HTML:
        try:
            nodes_json = json.dumps([node.to_dict() for node in nodes])
        except TypeError as e:
            raise self.unsupported_field_type_error(e, "node")
        try:
            rels_json = json.dumps([rel.to_dict() for rel in relationships])
        except TypeError as e:
            raise self.unsupported_field_type_error(e, "relationship")

        render_options_json = json.dumps(render_options.to_dict())

        container_id = str(uuid.uuid4())
        js_code = f"""
        var myNvl = new NVLBase.NVL(
            document.getElementById('{container_id}'),
            document.getElementById('tooltip'),
            {nodes_json},
            {rels_json},
            {render_options_json},
        );
        """
        full_code = self.library_code + js_code
        html_output = f"""
        <div id="{container_id}" style="width: {width}; height: {height}; position: relative;">
            <div id="tooltip" style="width: 20%; max-height: 90%; position: absolute; z-index: 2147483647; right: 0; bottom: 0; background: white; display: none; border: solid; border-color: #BBBEC3; border-width: 0.5px; padding: 0.6rem; border-radius: 8px; margin-bottom: 1rem; margin-right: 0.5rem; filter: drop-shadow(0 4px 8px rgba(26,27,29,0.12)); font: PublicSans; font-color: #4D5157; font-size: 14px"></div>
        </div>
        <script>
            {full_code}
        </script>
        """
        return HTML(html_output)  # type: ignore[no-untyped-call]
