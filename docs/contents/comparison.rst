How does :code:`easytree` compare with :code:`jsontree`
========================================================

:code:`easytree` differs from :code:`jsontree` (see `here <https://github.com/dougn/jsontree>`_) in three important ways:

1. elements, when attached or appended to an :code:`easytree.list`, recursively become :code:`easytree` types if they are themselves lists, sets, tuples, ranges, zips or dictionaries. 

Compare: 
::

    >>> import easytree

    >>> tree = easytree.dict()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this works
    >>> tree
    {
        'friends': [
            {'age': 29, 'name': 'David'},
            {'name': 'Celine'}
        ]
    }

with: 
:: 

    >>> import jsontree

    >>> tree = jsontree.jsontree()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this does not work
    AttributeError: 'dict' object has no attribute 'age'

2. :code:`easytree.dict` and :code:`easytree.list` objects inherit from the builtin :code:`dict` and :code:`list` objects, allowing for seamless integration into existing codebases

3. :code:`easytree.dict` and :code:`easytree.list` support freezing and sealing.


