# Graph Visualization for Python by Neo4j

[![Latest version](https://img.shields.io/pypi/v/neo4j-viz)](https://pypi.org/project/neo4j-viz/)
[![PyPI downloads month](https://img.shields.io/pypi/dm/neo4j-viz)](https://pypi.org/project/neo4j-viz/)
![Python versions](https://img.shields.io/pypi/pyversions/neo4j-viz)

`neo4j-viz` is a Python package for creating interactive graph visualizations.
The package wraps the [Neo4j Visualization JavaScript library (NVL)](https://neo4j.com/docs/nvl/current/).

Proper documentation is forthcoming.

**WARNING:**
This package is still in development and the API is subject to change.


## Some notable features

* Easy to import graphs represented as:
  * projections in the Neo4j Graph Data Science (GDS) library
  * pandas DataFrames
* Node features:
  * Sizing
  * Colors
  * Captions
  * Pinning
* Relationship features:
  * Colors
  * Captions
* Graph features:
  * Zooming
  * Panning
  * Moving nodes
  * Using different layouts
* Additional convenience functionality for:
  * Resizing nodes, optionally including scale normalization
  * Coloring nodes based on a property
  * Toggle whether nodes should be pinned or not

Please note that this list is by no means exhaustive.


![Example Graph](examples/example_cora_graph.png)


## Getting started

```
pip install neo4j-viz
```

inside the `python-wrapper` folder. This will install the Python package and make it available to Jupyter notebooks.

### Examples

For some Jupyter Notebook and streamlit examples, checkout the `/examples` directory.
