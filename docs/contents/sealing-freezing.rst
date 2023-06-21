Sealing and freezing 
=====================================
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

    >>> person = easytree.dict({"name":"Bob", "address":{"city":"New York"}}, sealed=True)
    >>> person.name = "Alice" # you can still edit leaf values
    >>> person.adress.city    # typo spelling address
    AttributeError: sealed node has no attribute 'adress'


You can :code:`seal` and :code:`unseal` a tree with the dedicated root-level functions. These functions return a *new* tree (i.e. these functions are not in-place).

Freezing
************************************
Freezing a tree prevents the user from accidentally creating new nodes or changing existing nodes. 
:: 

    >>> person = easytree.dict({"name":"Bob", "address":{"city":"New York"}}, frozen=True)
    >>> person.address.city = "Los Angeles"
    AttributeError: cannot set attribute 'city' on frozen node

You can :code:`freeze` and :code:`unfreeze` a tree with the dedicated root-level functions. These functions return a *new* tree (i.e. these functions are not in-place).
