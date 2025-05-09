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
        show_hover_tooltip: bool,
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

        if show_hover_tooltip:
            hover_element = f"document.getElementById('{container_id}-tooltip')"
            hover_div = f'<div id="{container_id}-tooltip" style="width: 20%; min-width: 100px; max-width: 600px; max-height: 80%; position: absolute; z-index: 2147483647; right: 0; bottom: 0; background: inherit; display: none; border: solid; border-color: #BBBEC3; border-width: 0.5px; padding: 0.8rem; border-radius: 8px; margin-bottom: 1rem; margin-right: 0.5rem; filter: drop-shadow(0 4px 8px rgba(26,27,29,0.12)); font-family: PublicSans; color: #aeaeae; font-size: 14px"></div>'
        else:
            hover_element = "null"
            hover_div = ""

        # Using a different varname for every instance, so that a notebook
        # can use several instances without unwanted interactions.
        # The first part of the UUID should be "unique enough" in this context.
        nvl_varname = "graph_" + container_id.split("-")[0]
        download_name = nvl_varname + ".png"

        js_code = f"""
        var {nvl_varname} = new NVLBase.NVL(
            document.getElementById('{container_id}'),
            {hover_element},
            {nodes_json},
            {rels_json},
            {render_options_json},
        );
        """
        full_code = self.library_code + js_code

        base_folder = files("neo4j_viz")
        resource_folder = base_folder / "resources"

        zoom_in_path = resource_folder / "zoom-in.svg"
        with zoom_in_path.open("r", encoding="utf-8") as file:
            zoom_in_svg = file.read()

        zoom_out_path = resource_folder / "zoom-out.svg"
        with zoom_out_path.open("r", encoding="utf-8") as file:
            zoom_out_svg = file.read()

        screenshot_path = resource_folder / "screenshot.svg"
        with screenshot_path.open("r", encoding="utf-8") as file:
            screenshot_svg = file.read()

        css = resource_folder / "styles.css"
        with css.open("r", encoding="utf-8") as file:
            css_data = file.read()

        html_output = f"""
        <style>
            {css_data}
        </style>
        <div style="position: absolute; z-index: 2147483647; right: 0; top: 0; padding: 1rem">
            <button type="button" onclick="{nvl_varname}.nvl.saveToFile({{ filename: '{download_name}' }})" class="icon">
                {screenshot_svg}
            </button>
            <button type="button" onclick="{nvl_varname}.nvl.setZoom({nvl_varname}.nvl.getScale() + 0.5)" class="icon">
                {zoom_in_svg}
            </button>
            <button type="button" onclick="{nvl_varname}.nvl.setZoom({nvl_varname}.nvl.getScale() - 0.5)" class="icon">
                {zoom_out_svg}
            </button>
        </div>
        <div id="{container_id}" style="width: {width}; height: {height}; position: relative;">
            {hover_div}
        </div>

        <script>
            getTheme = () => {{
                const backgroundColorString = window.getComputedStyle(document.body, null).getPropertyValue('background-color')
                const colorsArray = backgroundColorString.match(/\d+/g);
                const brightness = Number(colorsArray[0]) * 0.2126 + Number(colorsArray[1]) * 0.7152 + Number(colorsArray[2]) * 0.0722
                return brightness < 128 ? "dark" : "light"
            }}
            document.documentElement.className = getTheme()

            {full_code}
        </script>
        """

        return HTML(html_output)  # type: ignore[no-untyped-call]
