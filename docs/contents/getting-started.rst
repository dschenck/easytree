Getting started 
===============

Installing :code:`easytree` is simple with pip: 
::

    pip install easytree

Consider the following tree, as an example:
::

    config = easytree.dict({
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

The type of each newly-created node, unless given an explicit value, is initially :code:`undefined`, and can change into a list node, a dict node (e.g. :code:`memory`) or a value-node (e.g. :code:`512GB SSD`). The type of an undefined node is dynamically determined by subsequent interactions.

- if a list method (e.g. :code:`append`) is called on an undefined node, that node becomes a list node. 
- if a dict method (e.g. :code:`update`) is called on an undefined node, or an attribute is called on an undefined node (e.g. :code:`node.name`), or a key is retrieved (e.g. :code:`node["name"]`), that node becomes a dict node.
- any value appended or assigned at a node recursively becomes a node, whose type is determined by the type of the given value (list node for iterables (lists, tuples, sets, ranges and zips), dict node for dictionaries, value-nodes for other types).

Example: 
::

    >>> root = easytree.dict({"name":"David"})  # root is a dict node
    >>> root.colors = ["blue", "brown"]         # colors is a list node of strings
    >>> root.cities.append(name="Paris")        # cities is a list node of dict nodes
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