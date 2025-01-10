import os


def setup(app) -> None:  # type: ignore
    theme_path = os.path.abspath(os.path.dirname(__file__))
    app.add_html_theme("sphinx_neo4j", theme_path)
