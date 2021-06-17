easytree
======================================
`easytree <https://easytree.readthedocs.io/>`_ is a lightweight Python library, designed to easily create, serialize and read deeply-nested tree configurations.


.. image:: https://badge.fury.io/py/easytree.svg
   :target: https://badge.fury.io/py/easytree

.. image:: https://readthedocs.org/projects/easytree/badge/?version=latest
   :target: https://easytree.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/dd/easytree
   :target: https://img.shields.io/pypi/dd/easytree

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

Quickstart
-------------------------------------
Installing :code:`easytree` is simple with pip: 
::

    pip install easytree

Using :code:`easytree` is also easy
::
    
    >>> import easytree

    #let's create a deeply-nested chart configuration
    >>> chart = easytree.Tree()
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

Writing deeply-nested trees with list nodes is easy with a context-manager:
::

    >>> chart = easytree.Tree()
    >>> with chart.axes.append({}) as axis: 
    ...     axis.title.text = "primary axis"
    >>> with chart.axes.append({}) as axis: 
    ...     axis.title.text = "secondary axis"
    >>> chart.serialize()
    {
        "axes": [
            {
                "title": {
                    "text": "primary axis"
                }
            },
            {
                "title": {
                    "text": "secondary axis"
                }
            }
        ]
    }

Tutorial 
-------------------------------------------------------
Consider the following tree, as an example:
::

    config = easytree.Tree({
        "date":"2020-02-20",
        "size":{
            "height":"1.56 cm",
            "width":"30.41 cm"
        },
        "users":[
            "Alice",
            "Bob"
        ]
    })

There are three types of nodes in this tree: 

- value leaves (e.g. "2020-02-20", "1.56 cm" or "Alice")
- dict nodes (e.g. "size")
- list nodes (e.g. "users")

Instead of raising an :code:`AttributeError`, reading or setting a new attribute on a dict node creates and returns a new child node.
::

    >>> config.memory.size = "512GB SSD" #memory node is created on the fly
    >>> config
    {
        "date":"2020-02-20",
        "size":{
            "height":"1.56 cm",
            "width":"30.41 cm"
        },
        "users":[
            "Alice",
            "Bob"
        ]
        "memory":{
            "size": "512GB SSD"
        }
    }

You can recursively create list and dict nodes on the fly: 
:: 

    >>> config.events.append(name="create", user="Alice") #events node is created on the fly
    >>> config.events.append({"name:"edit", "user":"Bob"})
    >>> config
    {
        "date":"2020-02-20",
        "size":{
            "height":"1.56 cm",
            "width":"30.41 cm"
        },
        "users":[
            "Alice",
            "Bob"
        ]
        "memory":{
            "size": "512GB SSD"
        },
        "events":[
            {
                "name": "create", 
                "user": "Alice"
            },
            {
                "name": "edit", 
                "user": "Bob"
            }
        ]
    }

The type of each newly-created node, unless given an explicit value, is initially undefined, and can change into a list node, a dict node (e.g. :code:`memory`) or a value-node (e.g. :code:`512GB SSD`). The type of an undefined node is dynamically determined by subsequent interactions.

- if the :code:`append` method is called on an undefined node, that node becomes a list node. 
- if an attribute is called on an undefined node (e.g. :code:`node.name`), or a key is retrieved (e.g. :code:`node["name"]`), that node becomes a dict node.
- any value appended or assigned at a node recursively becomes a node, whose type is determined by the type of the given value (list node for iterables (list, tuple, set), dict node for dictionaries, value-nodes for other types).

Example: 
::

    >>> root = easytree.Tree()           #root is an undefined node
    >>> root.name = "David"              #root is now a dict node, and name is a string
    >>> root.colors = ["blue", "brown"]  #colors is a list node of strings
    >>> root.cities.append(name="Paris") #cities is a list node of dict nodes
    >>> root
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

.. note::
    A :code:`dict` node has only two methods: :code:`get` and :code:`serialize`. Any other attribute called on an instance will create a new node, attach it to the instance and return it.

    A :code:`list` node has only two methods: :code:`append` and :code:`serialize`. Any other attribute called on an instance raise an :code:`AttributeError`.

Once the type of a node is determined, it cannot morph into another type. For example:
::
    
    >>> root = easytree.Tree({}) #explicitely set as dict node
    >>> root.append(1)
    AttributeError: 'dict' object has no attribute 'append'

.. warning::
    For an undefined node, retrieving an integer key (e.g. :code:`node[0]`) is intrinsically ambiguous: did the user expect the first value of a list node (which should raise an :code:`IndexError` given that the list is then empty), or the value at the key :code:`0` of a dict node? **To avoid unintentionally creating dict nodes, an** :code:`AmbiguityError` **will be raised.**

How does :code:`easytree` compare with :code:`jsontree`
-------------------------------------------------------
:code:`easytree` differs from :code:`jsontree` (see `here <https://github.com/dougn/jsontree>`_) in two important ways:

1. elements, when attached or appended to an :code:`easytree.Tree`, recursively become tree branches if they are themselves lists, sets, tuples or dictionaries. 
2. serialization of an :code:`easytree.Tree` merely converts the tree to a dictionary, list or underlying value (for leaves). It does not serialize to JSON.
3. starting with 0.1.8, :code:`easytree` supports freezing or sealing trees to avoid accidentally create new nodes

Compare: 
::

    >>> import easytree

    >>> tree = easytree.Tree()
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

Sealing and freezing
-----------------------------------
.. note::

    New with version 0.1.8

While :code:`easytree` makes it easy to create deeply-nested trees, it can also make it error prone when reading back properties. 
Sealing and freezing allow to protect trees by restricting some or all mutations to a tree. 

+-----------------------+---------+--------+--------+
|                       | default | sealed | frozen |
+=======================+=========+========+========+
| read an existing node | ✅      | ✅     | ✅     |
+-----------------------+---------+--------+--------+
| create a new node     | ✅      | ❌     | ❌     |
+-----------------------+---------+--------+--------+
| edit a node           | ✅      | ✅     | ❌     |
+-----------------------+---------+--------+--------+
| delete a node         | ✅      | ❌     | ❌     |
+-----------------------+---------+--------+--------+


Sealing
************************************
Sealing a tree prevents the user from accidentally creating new nodes; it does allow to edit leaf values. 
::

    >>> person = easytree.Tree({"name":"Bob", "address":{"city":"New York"}}, sealed=True)
    >>> person.name = "Alice" #you can still edit leaf values
    >>> person.adress.city    #typo spelling address
    AttributeError: sealed node has no attribute 'adress'


You can :code:`seal` and :code:`unseal` a tree with the dedicated root-level functions. These functions return a *new* tree (i.e. these functions are not in-place).

Freezing
************************************
Freezing a tree prevents the user from accidentally creating new nodes or changing existing nodes. 
:: 

    >>> person = easytree.Tree({"name":"Bob", "address":{"city":"New York"}}, frozen=True)
    >>> person.address.city = "Los Angeles"
    AttributeError: cannot set attribute 'city' on frozen node

You can :code:`freeze` and :code:`unfreeze` a tree with the dedicated root-level functions. These functions return a *new* tree (i.e. these functions are not in-place).

API Documentation 
-----------------------------------
.. autoclass:: easytree.Tree
    :members:

.. autoclass:: easytree.Node
    :members:

.. automodule:: easytree
    :members: new, serialize, frozen, freeze, unfreeze, sealed, seal, unseal, load, loads, dump, dumps

Source code
-----------------------------------
The source code is hosted on `github <https://github.com/dschenck/easytree/>`_.

Changelog 
-----------------------------------

Version 0.1.0 (2020-08-01)
************************************
    - created :code:`easytree`

Version 0.1.1 (2020-08-02)
************************************
    - added ability to :code:`append` dictionary using keyword arguments
    - added ability to iterate over a tree
    - added ability to compute the length of a tree (for list nodes and dict nodes)

Version 0.1.2 (2020-08-03)
************************************
    - overrode the :code:`__new__` method to filter out primitive and object types
    - added ability to check for contains

Version 0.1.3 (2020-08-04)
************************************
    - added the :code:`serialize` method to the tree

Version 0.1.4 (2020-08-05)
************************************
    - added context manager to return a reference to itself
    - addressed infinite recursion in :code:`__getattr__`
    - :code:`append` now returns a reference to last added node, if it is a node

Version 0.1.5 (2020-08-08)
************************************
    - refactored the :code:`Tree` object into a :code:`Tree` and :code:`Node` object
    - removed the :code:`__new__` from the :code:`Tree` root object to allow for inheritence

Version 0.1.6 (2020-08-16)
************************************
    - fixed a bug where overriding an attribute would fail if it was already in the node

Version 0.1.7 (2021-05-01)
************************************
    - passing an :code:`easytree.Tree` object as an instanciation argument will copy the tree
    - added support for list slicing in list nodes
    - improved error messages
    - removed unncessary code in append method
    - factored out constants
    - :code:`repr` now delegates to underlying value
    - addressed ipython canary 
    - added :code:`get` method for dict nodes
    - implemented :code:`__delitem__`, :code:`__delattr__` and :code:`__bool__`

Version 0.1.8 (2021-06-13)
************************************
    - formatted code using `Black <https://github.com/psf/black>`_ 
    - added convenience i/o functions (e.g. :code:`load` and :code:`dump`)
    - added support for :code:`abc.KeysView` and :code:`abc.ValuesView` values
    - merged root and node classes
    - refactored :code:`__value__` attribute to :code:`_value`
    - added support for freezing and sealing trees
