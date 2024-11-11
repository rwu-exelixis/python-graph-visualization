import os
import uuid
from IPython.display import HTML

class NVL:
    def __init__(self):
        module_dir = os.path.dirname(__file__)
        js_path = os.path.join(module_dir, 'dist', 'base.js')

        with open(js_path, 'r', encoding='utf-8') as file:
            self.library_code = file.read()

    def render(self, nodes, relationships, options={}, width='100%', height='300px'):
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
        display(HTML(html_output))