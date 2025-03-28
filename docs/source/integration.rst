Integration with other libraries
================================

In addition to creating graphs from scratch, with ``neo4j-viz`` as is shown in the
:doc:`Getting started section <./getting-started>`, you can also import data directly from external sources.
In this section we will cover how to import data from `Pandas DataFrames <https://pandas.pydata.org/>`_ and
`Neo4j Graph Data Science <https://neo4j.com/docs/graph-data-science/current/>`_.


Pandas DataFrames
-----------------

The ``neo4j-viz`` library provides a convenience method for importing data from Pandas DataFrames.
It requires and additional dependency to be installed, which you can do by running:

.. code-block:: bash

    pip install neo4j-viz[pandas]

Once you have installed the additional dependency, you can use the :doc:`from_gds <./api-reference/from_pandas>` method
to import pandas DataFrames.

The ``from_dfs`` method takes two mandatory positional parameters:

* A Pandas ``DataFrame``, or iterable (eg. list) of DataFrames representing the nodes of the graph.
  The rows of the DataFrame(s) should represent the individual nodes, and the columns should represent the node
  IDs and properties. The columns map directly to fields of :doc:`Node <./api-reference/node>`, and as such
  should follow the same naming conventions.
* A Pandas ``DataFrame``, or iterable (eg. list) of DataFrames representing the relationships of the graph.
  The rows of the DataFrame(s) should represent the individual relationships, and the columns should represent the
  relationship IDs and properties. The columns map directly to fields of
  :doc:`Relationship <./api-reference/relationship>`, and as such should follow the same naming conventions.

``from_dfs`` also takes an optional property, ``node_radius_min_max``, that can be used (and is used by default) to
scale the node sizes for the visualization.
It is a tuple of two numbers, representing the radii (sizes) in pixels of the smallest and largest nodes respectively in
the visualization.
The node sizes will be scaled such that the smallest node will have the size of the first value, and the largest node
will have the size of the second value.
The other nodes will be scaled linearly between these two values according to their relative size.
This can be useful if node sizes vary a lot, or are all very small or very big.


Example
~~~~~~~

In this small example, we import a tiny toy graph representing a social network from two Pandas DataFrames.
As we can see the column names of the DataFrames map directly to the fields of :doc:`Nodes <./api-reference/node>`
and :doc:`Relationships <./api-reference/relationship>`.

.. code-block:: python

    from pandas import DataFrame
    from neo4j_viz.pandas import from_dfs

    nodes = DataFrame({
        "id": [1, 2, 3],
        "caption": ["Alice", "Bob", "Charlie"],
        "size": [20, 10, 10],
    })
    relationships = DataFrame({
        "source": [1, 2],
        "target": [2, 3],
        "caption": ["LIKES", "KNOWS"],
    })

    VG = from_dfs(nodes, relationships)

For another example of the ``from_dfs`` importer in action, see the
:doc:`Visualizing Snowflake Tables tutorial <./tutorials/snowpark-example>`.


Neo4j Graph Data Science (GDS) library
--------------------------------------

The ``neo4j-viz`` library provides a convenience method for importing data from the Neo4j Graph Data Science (GDS)
library.
It requires and additional dependency to be installed, which you can do by running:

.. code-block:: bash

    pip install neo4j-viz[gds]

Once you have installed the additional dependency, you can use the :doc:`from_gds <./api-reference/from_gds>` method
to import projections from the GDS library.

The ``from_gds`` method takes two mandatory positional parameters:

* An initialized ``GraphDataScience`` object for the connection to the GDS instance, and
* A ``Graph`` representing the projection that one wants to import.

We can also provide an optional ``size_property`` parameter, which should refer to a node property of the projection,
and will be used to determine the size of the nodes in the visualization.

The ``additional_node_properties`` parameter is also optional, and should be a list of additional node properties of the
projection that you want to include in the visualization.
For example, these properties could be used to color the nodes, or give captions to them in the visualization.

The last optional property, ``node_radius_min_max``, can be used (and is used by default) to scale the node sizes for
the visualization.
It is a tuple of two numbers, representing the radii (sizes) in pixels of the smallest and largest nodes respectively in
the visualization.
The node sizes will be scaled such that the smallest node will have the size of the first value, and the largest node
will have the size of the second value.
The other nodes will be scaled linearly between these two values according to their relative size.
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


Please see the :doc:`Visualizing Neo4j Graph Data Science (GDS) Graphs tutorial <./tutorials/gds-example>` for a
more extensive example.


Neo4j Database
---------------

The ``neo4j-viz`` library provides a convenience method for importing data from Neo4j.
It requires and additional dependency to be installed, which you can do by running:

.. code-block:: bash

    pip install neo4j-viz[neo4j]

Once you have installed the additional dependency, you can use the :doc:`from_neo4j <./api-reference/from_neo4j>` method
to import query results from Neo4j.

The ``from_neo4j`` method takes one mandatory positional parameters:

* A ``result`` representing the query result either in form of `neo4j.graph.Graph` or `neo4j.Result`.

The ``node_caption`` parameter is also optional, and indicates the value to use for the caption of each node in the visualization.

We can also provide an optional ``size_property`` parameter, which should refer to a node property of the projection,
and will be used to determine the size of the nodes in the visualization.

The last optional property, ``node_radius_min_max``, can be used (and is used by default) to scale the node sizes for
the visualization.
It is a tuple of two numbers, representing the radii (sizes) in pixels of the smallest and largest nodes respectively in
the visualization.
The node sizes will be scaled such that the smallest node will have the size of the first value, and the largest node
will have the size of the second value.
The other nodes will be scaled linearly between these two values according to their relative size.
This can be useful if node sizes vary a lot, or are all very small or very big.


Example
~~~~~~~

In this small example, we import a graph from a Neo4j query result.

.. code-block:: python

    from neo4j import GraphDataScience
    from neo4j_viz.gds import from_gds

    # Modify this to match your Neo4j instance's URI and credentials
    URI = "neo4j://localhost:7687"
    auth = ("neo4j", "password")

    with GraphDatabase.driver(URI, auth=auth) as driver:
        driver.verify_connectivity()

        result = driver.execute_query(
            "MATCH (n)-[r]->(m) RETURN n,r,m",
            database_="neo4j",
            result_transformer_=Result.graph,
        )

    VG = from_neo4j(result)


Please see the :doc:`Visualizing Neo4j Graphs tutorial <./tutorials/neo4j-example>` for a
more extensive example.
