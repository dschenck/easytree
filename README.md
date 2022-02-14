# easytree

[![build](https://github.com/dschenck/easytree/workflows/easytree/badge.svg)](https://github.com/dschenck/easytree/actions)
[![PyPI version](https://badge.fury.io/py/easytree.svg)](https://badge.fury.io/py/easytree) 
[![Documentation Status](https://readthedocs.org/projects/easytree/badge/?version=latest)](https://easytree.readthedocs.io/en/latest/?badge=latest) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight Python library designed to easily read and write deeply-nested tree configurations.

## Documentation
Documentation is hosted on [read the docs](https://easytree.readthedocs.io/en/latest/)

## Installation
```
pip install easytree
```

## Quickstart 
```python
>>> import easytree

>>> tree = easytree.Tree()
>>> tree.foo.bar.baz = "Hello world!"
>>> tree
Tree({
    "foo":{
        "bar":{
            "baz":"Hello world!"
        }
    }
})
```
