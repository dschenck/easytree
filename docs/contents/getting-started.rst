Getting started 
===============


Simply import :code:`easytree` and create nested nodes on the fly using the dot notation. 

.. code-block::

    >>> import easytree

    >>> tree = easytree.dict()
    >>> tree.foo.bar.baz = "Hello world!"
    >>> tree 
    {
        "foo": {
            "bar": {
                "baz": "Hello world!"
            }
        }
    }

Instead of raising an :code:`AttributeError`, reading or setting a new attribute on an :code:`easytree.dict` node creates and returns a new child node. Assigning or reading a value from the child node *casts* the node as an :code:`easytree.dict`. 

.. code-block:: 

    >>> tree = easytree.dict()
    >>> tree.address 
    <Node 'address'>

    >>> tree.address.country = "United States"
    >>> tree.address
    {"country": "United States"}


Alternatively, use a list method such as :code:`append` to cast a new node as a :code:`list`

.. code-block:: 

    >>> tree = easytree.dict()
    >>> tree.foo.bar.baz.append("Hello world!")
    >>> tree
    {
        "foo": {
            "bar": {
                "baz": ["Hello world!"]
            }
        }
    }

.. hint:: The :code:`baz` node *became* an :code:`easytree.list` node because a list method was called on it.

You can use the dot or bracket notation interchangeably

.. code-block:: 

    >>> tree = easytree.dict({"foo":"bar"})
    >>> tree["foo"]
    "bar"
    >>> tree.foo
    "bar"

.. hint:: The :code:`easytree.dict` *inherits* from the native python :code:`dict` class.

A dict node in (or appended to) an :code:`easytree.list` is always cast as an :code:`easytree.dict`, allowing you to use the dot notation throughout the tree.

.. code-block::

    >>> friends = easytree.list()
    >>> friends.append({"firstname":"Alice"})
    >>> friends[0].address.country = "Netherlands"
    >>> friends
    [
        {
            "firstname": "Alice",
            "address": {
                "country": "Netherlands"
            }
        }
    ]

Writing deeply-nested trees is made easy with a context-manager:

.. code-block:: 

    >>> order = easytree.dict()
    >>> with order.customer.delivery.address as a: 
    ...     a.country = "United States"
    ...     a.city    = "New York"
    ...     a.street  = "5th avenue"
    >>> order
    {
        "order": {
            "customer": {
                "delivery": {
                    "address": {
                        "country": "United States",
                        "city": "New York", 
                        "street": "5th avenue"
                    }
                }
            }
        }
    }

Because the append method returns a reference to the last-appended object, writing deeply-nested trees which combine :code:`easytree.dict` and :code:`easytree.list` nodes is also easy: 


.. hint:: The :code:`append` method of an :code:`easytree.list` returns the added value rather than :code:`None` to allow for the below syntax.

.. code-block::

    >>> profile = easytree.dict()
    >>> with profile.friends.append({"firstname":"Flora"}) as friend: 
    ...     friend.birthday = "25/02"
    ...     friend.address.country = "France"
    >>> profile
    {
        "friends": [
            {
                "firstname": "Flora",
                "birthday": "25/02",
                "address": {
                    "country": "France"
                }
            }
        ]
    }

The :code:`get` method is supercharged to query deeply-nested trees.

.. code-block:: 

    >>> profile = easytree.dict()
    >>> profile.friends.append({"name":"Bob", "address":{"country":"France"}})
    >>> profile.get(["friends", 0, "address", "country"])
    France
    >>> profile.get(["friends", 0, "address", "street"])
    None

.. hint:: Normally, this would raise an error, as a list is not hashable.


Pitfalls
--------
By definition, and unless an easytree is sealed or frozen, reading an undefined attribute will not raise an exception. 

.. code-block:: 

    >>> profile = easytree.dict({"firstname":"David"})
    >>> profile.firstnam #typo
    <Node 'firstnam'> 

Dictionary and lists added to an easytree will be *cast* to an :code:`easytree.dict` or :code:`easytree.list` object

.. code-block:: 

    >>> point = {"x":1, "y":1}
    >>> graph = easytree.list([point])
    >>> point in graph
    True
    >>> graph[0] is point 
    False