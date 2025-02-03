# Graph Visualization for Python by Neo4j

[![Latest version](https://img.shields.io/pypi/v/neo4j-viz)](https://pypi.org/project/neo4j-viz/)
[![PyPI downloads month](https://img.shields.io/pypi/dm/neo4j-viz)](https://pypi.org/project/neo4j-viz/)
![Python versions](https://img.shields.io/pypi/pyversions/neo4j-viz)
[![Documentation](https://img.shields.io/badge/Documentation-latest-blue)](https://development.neo4j.dev/docs/nvl-python/preview/)
[![Discord](https://img.shields.io/discord/787399249741479977?label=Chat&logo=discord)](https://discord.gg/neo4j)
[![Community forum](https://img.shields.io/website?down_color=lightgrey&down_message=offline&label=Forums&logo=discourse&up_color=green&up_message=online&url=https%3A%2F%2Fcommunity.neo4j.com%2F)](https://community.neo4j.com)
[![License](https://img.shields.io/pypi/l/neo4j-viz)](https://pypi.org/project/neo4j-viz/)

`neo4j-viz` is a Python package for creating interactive graph visualizations.
It focuses on convenience to visualize graphs from Neo4j Graph Data Science (GDS) projections.

The output is of type `IPython.display.HTML` and can be viewed directly in a Jupyter Notebook, Streamlit.
Alternatively, you can export the output to a file and view it in a web browser.

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

### Examples

For some Jupyter Notebook and streamlit examples, checkout the [/examples](/examples)  directory.


## Contributing

If you would like to contribute to this project, please follow our [Contributor Guidelines](./CONTRIBUTING.md).
