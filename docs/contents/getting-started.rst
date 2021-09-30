Getting started 
=====================================

Installing :code:`easytree` is simple with pip: 
::

    pip install easytree

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
    >>> config.events.append({"name":"edit", "user":"Bob"})
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