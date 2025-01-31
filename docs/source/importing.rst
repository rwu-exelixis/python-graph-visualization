Importing from external sources
===============================

In addition to creating graphs from scratch, with ``neo4j-viz`` as is shown in the
:doc:`Getting started section <./getting-started>`, you can also import data directly from external sources.
In this section we will cover how to import data from `Pandas DataFrames <https://pandas.pydata.org/>`_ and
`Neo4j Graph Data Science <https://neo4j.com/docs/graph-data-science/current/>`_.


Neo4j Graph Data Science (GDS) library
--------------------------------------

The ``neo4j-viz`` library provides a convenience method for importing data from the Neo4j Graph Data Science (GDS)
library.
It requires and additional dependency to be installed, which you can do by running:

.. code-block:: bash

    pip install neo4j-viz[gds]

Once you have installed the additional dependency, you can use the :doc:`from_gds <./api-reference/from_gds>` method
to import projections from the GDS library.

The ``from_dfs`` method takes two mandatory positional parameters:
* An initialized ``GraphDataScience`` object for the connection to the GDS instance, and
* A ``Graph`` representing the projection that one wants to import.

We can also provide an optional ``size_property`` parameter, which should refer to a node property of the projection, and
will be used to determine the size of the nodes in the visualization.

The ``additional_node_properties`` parameter is also optional, and should be a list of additional node properties of the
projection that you want to include in the visualization.
For example, these properties could be used to color the nodes, or give captions to them in the visualization.

The last optional property, ``node_radius_min_max``, can be used (and is used by default) to scale the node sizes for the
visualization.
It is a tuple of two floats, representing the radii (sizes) in pixels of the smallest and largest nodes respectively in
the visualization.
This can be useful if node sizes vary a lot, or are all very small or very big.


Example
~~~~~~~

In this small example, we import a graph projection from the GDS library, that has the node properties "pagerank" and
"componentId".
We use the "pagerank" property to determine the size of the nodes, and the "componentId" property to color the nodes.

.. code-block:: python

    from graphdatascience import GraphDataScience
    from neo4j_viz.gds import from_gds

    gds = GraphDataScience(...)
    G = gds.graph.project(...)

    # Compute the PageRank and Weakly Connected Components
    gds.pageRank.mutate(G, mutateProperty="pagerank")
    gds.wcc.mutate(G, mutateProperty="componentId")

    # Import the projection into a `VisualizationGraph`
    # Make sure to include `pagerank` and `componentId`
    VG = from_gds(
        gds,
        G,
        size_property="pagerank",
        additional_node_properties=["componentId"],
    )

    # Color the nodes by the `componentId` property, so that the nodes are
    # colored by the connected component they belong to
    VG.color_nodes("componentId")


Please see the :doc:`Visualizing Neo4j Graph Data Science (GDS) Graphs tutorial <./tutorials/gds-nvl-example>` for a
more extensive example.


Pandas DataFrames
-----------------

