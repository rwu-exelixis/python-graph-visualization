Customizing the visualization
=============================

Once created, a :doc:`VisualizationGraph object <./api-reference/visualization-graph>` can be modified in various ways
to adjust what the visualization looks like the next time you render it.
In this section we will discuss how to color, size, and pin nodes, as well as how to directly modify nodes and
relationships of existing ``VisualizationGraph`` objects.

If you have not yet created a ``VisualizationGraph`` object, please refer to one of the following sections:

* :doc:`Getting started <./getting-started>` for creating a visualization graph from scratch using ``neo4j-viz``
  primitives like :doc:`Node <./api-reference/node>` and :doc:`Relationship <./api-reference/relationship>` and
  :doc:`VisualizationGraph <./api-reference/visualization-graph>` directly. Or
* :doc:`Integration with other libraries <./integration>` for importing data from a Pandas DataFrame or Neo4j GDS
  projection.


Coloring nodes
--------------

Nodes can be colored directly by providing them with a color property, upon creation.
This can for example be done by passing a color as a string to the ``color`` parameter of the
:doc:`Node <./api-reference/node>` object.

Alternatively, you can color nodes based on a property (field) of the nodes after a ``VisualizationGraph`` object has been
created.


The ``color_nodes`` method
~~~~~~~~~~~~~~~~~~~~~~~~~~

By calling the :meth:`neo4j_viz.VisualizationGraph.color_nodes` method, you can color nodes based on a
node property (field).
This method will give a distinct color (if possible) to each unique value of the node ``property`` that you provide as
the first positional argument.

By default the Neo4j color palette that works for both light and dark mode will be used.
If you want to use a different color palette, you can pass a dictionary or iterable of colors as the ``colors``
parameter.
You can for example use the color palettes from the `palettable library <https://jiffyclub.github.io/palettable/>`_ as in
the following example:

.. code-block:: python

    from palettable.wesanderson import Moonrise1_5

    # VG is a VisualizationGraph object
    VG.color_nodes("caption", Moonrise1_5.colors)

In this case, all nodes with the same caption will get the same color.

If there are fewer colors that unique values for the node ``property`` provided, the colors will be reused in a cycle.
To avoid that, you could use another palette or extend one with additional colors. Please refer to the
:doc:`Visualizing Neo4j Graph Data Science (GDS) Graphs tutorial <./tutorials/gds-example>` for an example on how
to do the latter.

If some nodes already have a ``color`` set, you can choose whether or not to override it with the ``override``
parameter.


Sizing nodes
--------------

Nodes can be given a size directly by providing them with a size property, upon creation.
This can for example be done by passing a size as an integer to the ``size`` parameter of the
:doc:`Node <./api-reference/node>` object.

Alternatively, you can size nodes after a ``VisualizationGraph`` object has been created.


The ``resize_nodes`` method
~~~~~~~~~~~~~~~~~~~~~~~~~~~

By calling the :meth:`neo4j_viz.VisualizationGraph.resize_nodes` method, you can resize nodes by:

* passing new nodes sizes as a dictionary ``sizes``, mapping node IDs to sizes in pixels, or
* providing a tuple of two numbers ``node_radius_min_max``: minimum and maximum radii (sizes) in pixels to which the
  nodes will be scaled.

Or you could provide both ``sizes`` and ``node_radius_min_max``, in which case the dictionary will be used to first set
the sizes of the nodes, and then the minimum and maximum values of the tuple will be subsequently used to scale the
sizes to the provided range.

If you provide only the ``node_radius_min_max`` parameter, the sizes of the nodes will be scaled such that the smallest
node will have the size of the first value, and the largest node will have the size of the second value.
The other nodes will be scaled linearly between these two values according to their relative size.
This can be useful if node sizes vary a lot, or are all very small or very big.

In the following example, we resize the node with ID 42 to have a size of 88 pixels, and then scales all nodes to have
sizes between 5 and 20 pixels:

.. code-block:: python

    # VG is a VisualizationGraph object
    VG.resize_nodes(sizes={42: 88}, node_radius_min_max=(5, 20))

Please note that means that also the node with ID 42 will be scaled to be between 5 and 20 pixels in size.


Pinning nodes
-------------

Nodes can be pinned to their current position in the visualization, so that they will not be moved by the force-directed
layout algorithm.
This can be useful if you want to keep a node in a specific position, for example to highlight it.

Nodes can be pinned directly upon creation.
This can for example be done by passing ``pinned=True`` to the :doc:`Node <./api-reference/node>` object.

Alternatively, you can toggle node pinning after a ``VisualizationGraph`` object has been created.


The ``toggle_nodes_pinned`` method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By calling the :meth:`neo4j_viz.VisualizationGraph.toggle_nodes_pinned` method, you can toggle whether nodes should be
pinned or not.
This method takes dictionary that maps node IDs to boolean values, where ``True`` means that the node is pinned, and
``False`` means that the node is not pinned.

In the following example, we pin the node with ID 1337 and unpin the node with ID 42:

.. code-block:: python

    # VG is a VisualizationGraph object
    VG.toggle_nodes_pinned(1337: True, 42: False)})


Direct modification of nodes and relationships
----------------------------------------------

Nodes and relationships can also be modified directly by accessing the ``nodes`` and ``relationships`` attributes of an
existing ``VisualizationGraph`` object.
These attributes list of all the :doc:`Nodes <./api-reference/node>` and
:doc:`Relationships <./api-reference/relationship>` in the graph, respectively.

Each node and relationship has attributes that can be accessed and modified directly, as in the following example:

.. code-block:: python

    # VG is a VisualizationGraph object
    VG.nodes[0].size = 10
    VG.relationships[4].caption = "BUYS"

Any changes made to the nodes and relationships will be reflected in the next rendering of the graph.
