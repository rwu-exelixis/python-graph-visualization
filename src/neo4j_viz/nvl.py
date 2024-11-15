import uuid
from importlib.abc import Traversable
from importlib.resources import files
from typing import Any

from IPython.display import HTML


class NVL:
    def __init__(self) -> None:
        js_path: Traversable = files("neo4j_viz.resources.nvl_entrypoint") / "base.js"

        with js_path.open("r", encoding="utf-8") as file:
            self.library_code = file.read()

    def render(
        self,
        nodes: list[dict[str, Any]],
        relationships: list[dict[str, Any]],
        options: dict[str, Any] = {},
        width: str = "100%",
        height: str = "300px",
    ) -> HTML:
        container_id = str(uuid.uuid4())
        js_code = f"""
        var myNvl = new NVLBase.NVL(
            document.getElementById('{container_id}'),
            {nodes},
            {relationships},
            {options}
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
