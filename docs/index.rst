easytree
========
A recursive dot-styled defaultdict to read and write deeply-nested trees

.. image:: https://github.com/dschenck/easytree/workflows/easytree/badge.svg
    :target: https://github.com/dschenck/easytree/actions

.. image:: https://badge.fury.io/py/easytree.svg
   :target: https://badge.fury.io/py/easytree

.. image:: https://readthedocs.org/projects/easytree/badge/?version=latest
   :target: https://easytree.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. image:: https://codecov.io/gh/dschenck/easytree/branch/master/graph/badge.svg?token=CPJXDL17CB 
   :target: https://codecov.io/gh/dschenck/easytree

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

.. toctree::
   :maxdepth: 2
   :caption: Table of contents

   contents/installation
   contents/getting-started
   contents/sealing-freezing
   contents/comparison
   contents/API
   contents/changelog