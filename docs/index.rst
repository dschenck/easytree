easytree
========
A recursive dot-styled defaultdict to read and write deeply-nested trees

.. include:: fragments/badges.rst

Quickstart
-------------------------------------
Installing :code:`easytree` is simple with pip: 
::

    pip install easytree

Simply import :code:`easytree` and create nested :code:`dict` nodes on the fly using the dot notation

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

Or use a list method such as :code:`append` to dynamically cast a new node as a :code:`list`

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

Find out more about what :code:`easytree` can do on the **Getting Started** page. 

Table of contents
-----------------

.. toctree::
   :maxdepth: 1

   contents/installation
   contents/getting-started
   contents/sealing-freezing
   contents/comparison
   contents/API
   contents/changelog