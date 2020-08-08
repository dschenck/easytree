# easytree

[![PyPI version](https://badge.fury.io/py/easytree.svg)](https://badge.fury.io/py/easytree) [![Documentation Status](https://readthedocs.org/projects/easytree/badge/?version=latest)](https://easytree.readthedocs.io/en/latest/?badge=latest) 

A fluent tree builder, useful to create multi-level, nested JSON configurations.

## Documentation
Documentation is hosted on [read the docs](https://easytree.readthedocs.io/en/latest/)

## Installation
```
pip install easytree
```

## Quickstart 
```python
>>> import easytree

#let's create a chart configuration
>>> chart = easytree.new()
>>> chart.chart.type = "bar"
>>> chart.title.text = "France Olympic Medals"
>>> chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
>>> chart.yAxis.title.text = "Count"
>>> chart.series.append(name="2016", data=[10, 18, 14])
>>> chart.series.append({"name":"2012"}) #list items recursively become nodes
>>> chart.series[1].data = [11, 11, 13]  #... as such, you can attach attributes

>>> chart.serialize()
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
```
