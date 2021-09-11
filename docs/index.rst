easytree
======================================
`easytree <https://easytree.readthedocs.io/>`_ is a lightweight Python library designed to easily read and write deeply-nested tree configurations.

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

Writing configurations that combine both list and dict nodes is easy - here's an example of an Highcharts chart configuration
::
    
    >>> import easytree

    >>> chart = easytree.Tree()
    >>> chart.chart.type = "bar"
    >>> chart.title.text = "France Olympic Medals"
    >>> chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
    >>> chart.yAxis.title.text = "Count"
    >>> chart.series.append(name="2016", data=[10, 18, 14])
    >>> chart.series.append({"name":"2012"})
    >>> chart.series[1].data = [11, 11, 13] #list items recursively become nodes

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

Writing deeply-nested trees with list nodes is easy with a context-manager:
::

    >>> chart = easytree.Tree()
    >>> with chart.axes.append({}) as axis: 
    ...     axis.title.text = "primary axis"
    ...     axis.min = 0
    >>> chart.serialize()
    {
        "axes": [
            {
                "title": {
                    "text": "primary axis"
                }
                "min":0
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