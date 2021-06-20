How does :code:`easytree` compare with :code:`jsontree`
========================================================

:code:`easytree` differs from :code:`jsontree` (see `here <https://github.com/dougn/jsontree>`_) in three important ways:

1. elements, when attached or appended to an :code:`easytree.Tree`, recursively become tree branches if they are themselves lists, sets, tuples or dictionaries. 

Compare: 
::

    >>> import easytree

    >>> tree = easytree.Tree()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this works
    >>> tree
    {'friends': [{'age': 29, 'name': 'David'}, {'name': 'Celine'}]}

with: 
:: 

    >>> import jsontree

    >>> tree = jsontree.jsontree()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this does not work
    AttributeError: 'dict' object has no attribute 'age'

2. serialization of an :code:`easytree.Tree` merely converts the tree to a dictionary, list or underlying value (for leaves). It does not serialize to JSON-string.

For example: 
::

    >>> import easytree

    >>> tree = easytree.Tree()
    >>> tree.abc.xyz = [1,2,3]
    >>> isinstance(tree.serialize(), dict)
    True
    >>> isinstance(tree.serialize()["abc"]["xyz"], list)
    True

3. starting with version 0.1.8, :code:`easytree` supports freezing and sealing trees.


