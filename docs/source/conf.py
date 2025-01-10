# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import pathlib


project = "Graph Visualization for Python"
copyright = "2025, Neo4j, Inc."
author = "Neo4j, Inc."
release = "0.1.6"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # include docs from docstrings
    "enum_tools.autoenum",  # specialised autoclass for enums
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


# use neo4j theme, which extends neo4j docs css for sphinx
html_theme = "neo4j"
theme_path = pathlib.Path(__file__).resolve().parent
print(theme_path)
html_static_path = [str(theme_path / "themes")]


# 01-nav.js is a copy of a js file of the same name that is included in the docs-ui bundle
def setup(app):  # type: ignore
    app.add_js_file("https://neo4j.com/docs/assets/js/site.js", loading_method="defer")
    app.add_js_file("js/12-fragment-jumper.js", loading_method="defer")
    app.add_js_file("js/deprecated.js", loading_method="defer")


rst_epilog = """
.. |api-version| replace:: {versionnum}
""".format(
    versionnum=release,
)
