easytree
======================================
An easy and permissive python tree builder. 

Quickstart
-------------------------------------
Installing :code:`easytree` is simple with pip: 
::

    $ pip install easytree

Using :code:`easytree` is also easy
::
    
    >>> import json
    >>> import easytree

    #let's create a highchart chart configuration
    >>> chart = easytree.new()
    >>> chart.chart.type = "bar"
    >>> chart.title.text = "France Olympic Medals"
    >>> chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
    >>> chart.yAxis.title.text = "Count"
    >>> chart.series.append({"name":"2016", "data":[10, 18, 14]})
    >>> chart.series.append({"name":"2012"})
    >>> chart.series[1].data = [11, 11, 13] #whoops, forgot to set the data

    >>> easytree.serialize(chart)

    {
        "chart": {
            "type": "bar"
        },
        "title": {
            "text": "France Olympic Medals"
        },
        "xAxis": {
            "categories": [
                "Gold",
                "Silver",
                "Bronze"
            ]
        },
        "yAxis": {
            "title": {
                "text": "Count"
            }
        },
        "series": [
            {
                "name": "2016",
                "data": [
                    10,
                    18,
                    14
                ]
            },
            {
                "name": "2012",
                "data": [
                    11,
                    11,
                    13
                ]
            }
        ]
    }

How does :code:`easytree` compare with :code:`jsontree`
-------------------------------------------------------
:code:`easytree` differs from :code:`jsontree` (see `here <https://github.com/dougn/jsontree>`_) in two important ways:

1. list elements, when appended to an :code:`easytree`, recursively become tree branches if they are themselves lists, sets, tuples or dictionaries. 
2. :code:`easytree` is designed to make building a tree easier for the user, regardless of the datatype of the tree leaves; in other words, serialization of an :code:`easytree` merely converts the tree to a dictionary, list or underlying value (for leaves)

Compare: 
::

    >>> import easytree

    >>> tree = easytree.new()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this works
    >>> easytree.serialize(tree)

    {'friends': [{'age': 29, 'name': 'David'}, {'name': 'Celine'}]}

with: 
:: 

    >>> import jsontree

    >>> tree = jsontree.jsontree()
    >>> tree.friends = [{"name":"David"},{"name":"Celine"}]
    >>> tree.friends[0].age = 29 #this does not work
    
    AttributeError: 'dict' object has no attribute 'age'


API Documentation 
-----------------------------------
.. autoclass:: easytree.Tree
    :members:

.. automodule:: easytree
    :members: new, serialize