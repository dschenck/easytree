easytree
======================================
An easy and permissive python tree builder, useful to create multi-level JSON configurations. Think of an easytree as a recursive defaultdict which can morph into a list.

Quickstart
-------------------------------------
Installing :code:`easytree` is simple with pip: 
::

    $ pip install easytree

Using :code:`easytree` is also easy
::
    
    >>> import easytree

    #let's create a chart configuration
    >>> chart = easytree.new()
    >>> chart.chart.type = "bar"
    >>> chart.title.text = "France Olympic Medals"
    >>> chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
    >>> chart.yAxis.title.text = "Count"
    >>> chart.series.append(name="2016", data=[10, 18, 14])
    >>> chart.series.append({"name":"2012"})
    >>> chart.series[1].data = [11, 11, 13] #list items recursively become nodes

    >>> easytree.serialize(chart)
    {
        "chart": {
            "type": "bar"
        },
        "title": {
            "text": "France Olympic Medals"
        },
        "xAxis": {
            "categories": [
                "Gold",
                "Silver",
                "Bronze"
            ]
        },
        "yAxis": {
            "title": {
                "text": "Count"
            }
        },
        "series": [
            {
                "name": "2016",
                "data": [
                    10,
                    18,
                    14
                ]
            },
            {
                "name": "2012",
                "data": [
                    11,
                    11,
                    13
                ]
            }
        ]
    }

The name of the game: key assumptions
-------------------------------------------------------
The type of each newly-created node (including the root node), unless given an explicit value, is undefined, and can morph into a list-node, a dict-node or a value-node. The type of an undefined node is determined by subsequent interactions:

- if the :code:`append` method is called on an undefined node, that node becomes a list-node. 
- if an attribute is called on an undefined node (e.g. :code:`node.name`), or a key is retrieved (e.g. :code:`node["name"]`), that node becomes a dict-node.
- any value assigned at a node recursively becomes a node, whose type is determined by the type of the given value (list-node for iterables (list, tuple, set), dict-node for dictionaries, value-nodes for other types).

Example: 
::

    >>> root = easytree.new()            #root is an undefined node
    >>> root.name = "David"              #root is now a dict-node, and name is a string
    >>> root.colors = ["blue", "brown"]  #colors is a list-node of strings
    >>> root.cities.append(name="Paris") #cities is a list node of dict-nodes
    
    >>> easytree.serialize(root)
    {
        "name": "David",
        "colors": [
            "blue",
            "brown"
        ],
        "cities": [
            {
                "name": "Paris"
            }
        ]
    }

.. warning::
    For an undefined node, retrieving an integer key (e.g. :code:`node[0]`) is intrinsically ambiguous: did the user expect the first value of a list-node (which should raise an :code:`IndexError` given that the list is then empty), or the value at the key :code:`0` of a dict-node? 
    
    **To avoid unintentionally creating dict-nodes, an** :code:`IndexError` **will be raised.**

Once the type of a node is determined, it cannot morph into another type. For example:
::
    
    >>> root = easytree.tree({}) #explicitely set as dict-node
    >>> root.append(1)
    AttributeError: 'dict' object has no attribute 'append'

How does :code:`easytree` compare with :code:`jsontree`
-------------------------------------------------------
:code:`easytree` differs from :code:`jsontree` (see `here <https://github.com/dougn/jsontree>`_) in two important ways:

1. list elements, when appended to an :code:`easytree`, recursively become tree branches if they are themselves lists, sets, tuples or dictionaries. 
2. :code:`easytree` is designed to make building a tree easier for the user, regardless of the datatype of the tree leaves; in other words, serialization of an :code:`easytree` merely converts the tree to a dictionary, list or underlying value (for leaves)

Compare: 
::

    >>> import easytree

    >>> tree = easytree.new()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this works
    >>> easytree.serialize(tree)
    {'friends': [{'age': 29, 'name': 'David'}, {'name': 'Celine'}]}

with: 
:: 

    >>> import jsontree

    >>> tree = jsontree.jsontree()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this does not work
    AttributeError: 'dict' object has no attribute 'age'


API Documentation 
-----------------------------------
.. autoclass:: easytree.Tree
    :members:

.. automodule:: easytree
    :members: new, serialize

Changelog 
-----------------------------------

Version 0.1.0 (2020-08-01)
************************************
    - created :code:`easytree`

Version 0.1.1 (2020-08-02)
************************************
    - added ability to :code:`append` dictionary using keyword arguments
    - :code:`append` now delegates to underlying value object if it is not a list-node
    - added ability to iterate over a tree
    - added ability to compute the length of a tree (for list-nodes and dict-nodes)

Version 0.1.2 (2020-08-03)
************************************
    - overrode the :code:`__new__` method to filter out primitive and object types
    - added ability to check for contains