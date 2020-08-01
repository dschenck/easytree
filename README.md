[![Documentation Status](https://readthedocs.org/projects/easytree/badge/?version=latest)](https://easytree.readthedocs.io/en/latest/?badge=latest)


# easytree
 An easy and permissive python tree builder

## Installation
> pip install easytree

## Quickstart 
```python
import easytree

chart = easytree.new()
chart.chart.type = "bar"
chart.title.text = "France Olympic Medals"
chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
chart.yAxis.title.text = "Count"
chart.series.append({"name":"2016", "data":[10, 18, 14]})
chart.series.append({"name":"2012"})
chart.series[1].data = [11, 11, 13]

easytree.serialize(chart)

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

## Documentation
Documentation is hosted on [read the docs](https://easytree.readthedocs.io/en/latest/)
