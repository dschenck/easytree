easytree
========
recursive dot-styled dict and list to read and write deeply-nested trees

.. image:: https://github.com/dschenck/easytree/workflows/easytree/badge.svg
    :target: https://github.com/dschenck/easytree/actions

.. image:: https://badge.fury.io/py/easytree.svg
   :target: https://badge.fury.io/py/easytree

.. image:: https://readthedocs.org/projects/easytree/badge/?version=latest
   :target: https://easytree.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

Quickstart
-------------------------------------
Installing :code:`easytree` is simple with pip: 
::

    pip install easytree

Using :code:`easytree` is also easy
::

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

Creating trees that combine both list and dict nodes is easy
::

    >>> friends = easytree.list()
    >>> friends.append({"firstname":"Alice"})
    >>> friends[0].address.country = "Netherlands"
    >>> friends[0]["interests"].append("science")
    >>> friends
    [
        {
            "firstname": "Alice",
            "address": {
                "country": "Netherlands"
            },
            "interests": [
                "science"
            ]
        }
    ]

Writing deeply-nested trees with list nodes is easy with a context-manager:
::

    >>> profile = easytree.dict()
    >>> with profile.friends.append({"firstname":"Flora"}) as friend: 
    ...     friend.birthday = "25/02",
    ...     friend.address.country = "France
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

.. toctree::
   :maxdepth: 2
   :caption: Table of contents

   contents/installation
   contents/getting-started
   contents/sealing-freezing
   contents/comparison
   contents/API
   contents/changelog