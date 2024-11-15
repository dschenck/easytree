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

Inheritence 
-----------

:code:`easytree.dict` *inherits* from the native python :code:`dict` class.

.. code-block:: 

    >>> tree = easytree.dict({"foo":"bar"})
    >>> isinstance(tree, dict) 
    True

:code:`easytree.list` also inherits from the native python :code:`list` class. 

.. code-block:: 

    >>> numbers = easytree.list([1,3,5])
    >>> isinstance(numbers, list)
    True

Setting or assigning values
---------------------------

Instead of raising an :code:`AttributeError`, reading a new attribute on an :code:`easytree.dict` returns a new :code:`undefined` node. 

.. code-block:: 

    >>> tree = easytree.dict()
    >>> tree.address # undefined node
    <undefined 'address'>

Reading or setting an attribute on such child node dynamically *casts* it as an :code:`easytree.dict` and assigns it to its parent. 

.. code-block:: 

    >>> tree.address.country = "United States"
    >>> tree.address # now a dict
    {"country": "United States"}


Alternatively, using a list method such as :code:`append` dynamically *casts* the new node as an :code:`easytree.list`

.. code-block:: 

    >>> tree = easytree.dict()
    >>> tree.address # undefined node
    <undefined 'address'>

    >>> tree.address.country.append("United States")
    >>> tree.address # now a dict
    {"country": ["United States"]}


.. note:: 
    Technically, *casting* replaces the node with an appropriate class instance (e.g. dict or list) in the parent object

Of course, you can use the dot or bracket notation interchangeably, both to read and assign nested values

.. code-block:: 

    >>> tree = easytree.dict({"foo":"bar"})
    >>> tree["foo"]
    "bar"
    >>> tree.foo
    "bar"

.. note:: 
    The bracket notation remains necessary if the key is not a valid attribute identifier name, or if the key is identical to a :code:`dict` method name.
    
    .. code-block:: 

     >>> tree = easytree.dict()
     >>> tree["attribute with space"] = True
     >>> tree 
     {"attribute with space": True}



Nested assignment
-----------------

Dictionaries assigned to an :code:`easytree.dict` or added to an :code:`easytree.list` are themselves cast as :code:`easytree.dict` instances, allowing you to use the dot notation on nested dictionaries.

.. code-block::

    >>> friends = easytree.list()
    >>> friends.append({"firstname": "Alice"})
    >>> isinstance(friends[0], easytree.dict)
    True
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
    

Lists assigned to an :code:`easytree.dict` are also *cast* as :code:`easytree.list` instances.

.. code-block:: 

    >>> tree = easytree.dict({"numbers": [1,3,5]})
    >>> isinstance(tree.numbers, easytree.list)
    True

Tuple values assigned to an :code:`easytree.dict` are also *cast* as tuples of :code:`easytree` objects. 

.. code-block:: 

    >>> tree = easytree.dict({"country": ("France", {"capital": "Paris"})}) 
    >>> isinstance(tree.country, tuple)
    True
    >>> tree.country[0] 
    'France'
    >>> tree.country[0].capital 
    'Paris'


Getter
------

The :code:`get` method of :code:`easytree.dict` is supercharged to query deeply-nested trees.

.. code-block:: 

    >>> profile = easytree.dict()
    >>> profile.friends.append({"name":"Bob", "address":{"country":"France"}})
    >>> profile.get(["friends", 0, "address", "country"])
    France
    >>> profile.get(["friends", 0, "address", "street"])
    None

.. hint:: Normally, this would raise an error, as a list is not hashable. This means no collisions are possible between keys and such list queries.

Context manager
---------------

The context manager returns the node, such that writing deeply-nested trees is easier:

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

Because the :code:`append` method returns a reference to the last appended item, writing deeply-nested trees which combine :code:`easytree.dict` and :code:`easytree.list` nodes is also easy: 

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

The undefined node
------------------
An :code:`undefined` node object is returned when an undefined attribute is read from an :code:`easytree.dict` node. This falsy object contains a reference to its parent object, as well as the key from which this object was returned. 

.. code-block:: 

    >>> person = easytree.dict()
    >>> person.address 
    <undefined 'address'> 

Assigning or reading an attribute from an :code:`undefined` node *casts* it as a dictionary. This is possible since the :code:`undefined` object keeps a reference to its parent and the key from which it was returned. 

.. code-block:: 

    >>> person = easytree.dict()
    >>> person.address.country = "Nigeria"
    >>> person.address
    {"country": "Nigeria"}

Using the bracket notation works identically. 

.. code-block:: 

    >>> person = easytree.dict()
    >>> person["address"].country = "Nigeria"
    >>> person.address
    {"country": "Nigeria"}

An :code:`undefined` node evaluates to :code:`False`. 

.. code-block:: 

    >>> person = easytree.dict()
    >>> if not person.address:
    ...     print("address is missing")
    address is missing

Pitfalls
--------
By definition, and unless an easytree is sealed or frozen, reading an undefined attribute will not raise an exception. 

.. code-block:: 

    >>> profile = easytree.dict({"firstname":"David"})
    >>> profile.firstnam #typo
    <undefined 'firstnam'> 

Using a numeric key on an undefined node will cast the node as a dictionary, not a list. 

.. code-block:: 

    >>> profile = easytree.dict({"firstname":"David"})
    >>> profile.friends[0].name = "Flora"
    >>> profile
    {
        "friends": {
            0: "Flora"
        }
    }

Dictionary and lists added to an easytree are *cast* to an :code:`easytree.dict` or :code:`easytree.list` instance. This means identity is not preserved.

.. code-block:: 

    >>> point = {"x":1, "y":1}
    >>> graph = easytree.list([point])
    >>> point in graph
    True
    >>> graph[0] is point 
    False
