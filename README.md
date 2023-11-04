# easytree
[![pythons](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/easytree)
[![build](https://github.com/dschenck/easytree/workflows/easytree/badge.svg)](https://github.com/dschenck/easytree/actions)
[![PyPI version](https://badge.fury.io/py/easytree.svg)](https://badge.fury.io/py/easytree) 
[![Documentation Status](https://readthedocs.org/projects/easytree/badge/?version=latest)](https://easytree.readthedocs.io/en/latest/?badge=latest) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://codecov.io/gh/dschenck/easytree/branch/master/graph/badge.svg?token=CPJXDL17CB )](https://codecov.io/gh/dschenck/easytree)

A recursive dot-styled defaultdict to read and write deeply-nested trees

## Documentation
Documentation is hosted on [read the docs](https://easytree.readthedocs.io/en/latest/)

## Installation
```
pip install easytree
```

## Quickstart 
```python
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
```

Creating trees that combine both list and dict nodes is easy
```python
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
```

Writing deeply-nested trees with list nodes is easy with a context-manager:
```python
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
```
