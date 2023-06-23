Alternatives
========================================================
:code:`easytree` shares some functionality with other existing libraries, but differs from each in some respect.

:code:`collections.defaultdict`
-----------------------------------------------------------------------
The recursive nature of the :code:`easytree.dict` can be replicated with the native :code:`collections.defaultdict`. 

.. code-block:: 

    >>> import collections

    >>> recursivedict = lambda: collections.defaultdict(lambda: recursivedict())
    >>> data = recursivedict()
    >>> data["foo"]["bar"]["baz"] = "Hello world!"
    >>> data
    {
        "foo": {
            "bar": {
                "baz": "Hello world!"
            }
        }
    }

**However**

1. :code:`easytree.dict` allows for the dot notation

2. new nodes in an :code:`easytree.dict` can become a new :code:`easytree.dict` *or* :code:`easytree.list`.

.. code-block:: 

    >>> import easytree

    >>> data = easytree.dict()
    >>> data.foo.bar.baz.append("Hello world!")
    >>> data
    {
        "foo": {
            "bar": {
                "baz": ["Hello world!"]
            }
        }
    }


:code:`dictdot`
------------------------------------------------------
:code:`dictdot` is an alternative library (see `here <https://pypi.org/project/dictdot/>`_) which allows for the use of the dot notation.

**However**

1. :code:`easytree` allows you to recursively write new nested nodes

Compare:

.. code-block:: 

    >>> import easytree

    >>> data = easytree.dict()
    >>> data.foo.bar.baz = "Hello world!"
    >>> data 
    {
        "foo": {
            "bar": {
                "baz": "Hello world!"
            }
        }
    }

with 

.. code-block:: 

    >>> from dictdot import dictdot
    
    >>> data = dictdot()
    >>> data.foo.bar.baz
    AttributeError: 'NoneType' object has no attribute 'bar'

:code:`jsontree`
-------------------------------------------------------
Another competing alternative is :code:`jsontree` (see `here <https://github.com/dougn/jsontree>`_)

**However**

1. dictionaries and lists, when attached or appended to an :code:`easytree.list`, are recursively cast as :code:`easytree.dict` and :code:`easytree.list`. 

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

.. code-block:: 

    >>> data = easytree.dict({"foo":"bar"})
    >>> isinstance(data, dict)
    True

    >>> items = easytree.list([1,2,3])
    >>> isinstance(items, list)
    True


3. :code:`easytree.dict` and :code:`easytree.list` support freezing and sealing.


