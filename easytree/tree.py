class Tree:
    """
    Recursive tree
    """
    __hash__ = None 
    
    def __new__(cls, value=None): 
        if value is None or isinstance(value, (list, tuple, set, dict)):
            return super(Tree, cls).__new__(cls)
        return value

    def __init__(self, value=None):
        if isinstance(value, dict):
            value = {k:Tree(v) for k,v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            value = [Tree(v) for v in value]
        elif isinstance(value, Tree):
            value = value.__value__
        self.__value__ = value
        
    def __repr__(self):
        return f"<Tree type={self.__nodetype__}>"
    
    def __str__(self):
        return str(serialize(self))
        
    @property
    def __nodetype__(self): 
        if self.__value__ is None: 
            return "null"
        if isinstance(self.__value__, list):
            return "list"
        if isinstance(self.__value__, dict):
            return "dict"
        raise RuntimeError
    
    def __getattr__(self, name):
        if self.__nodetype__ in ["null", "dict"]:
            if self.__nodetype__ == "null":
                self.__value__ = {}
            if name not in self.__value__: 
                self.__value__[name] = Tree()
            return self.__value__[name]
        raise RuntimeError
    
    def __setattr__(self, name, value):
        if name == "__value__":
            return super().__setattr__(name, value)
        if self.__nodetype__ == "null":
            self.__value__ = {}
        if self.__nodetype__ == "dict": 
            if name not in self.__value__: 
                self.__value__[name] = Tree(value)
            self.__value__[name]
            return
        raise RuntimeError
        
    def __getitem__(self, name):
        if self.__nodetype__ == "null":
            if isinstance(name, int): 
                raise IndexError("list index out of range")
            else:
                self.__value__ = {}
        if self.__nodetype__ == "dict": 
            if name not in self.__value__: 
                self.__value__[name] = Tree()
            return self.__value__[name]
        if self.__nodetype__ == "list": 
            if not isinstance(name, int): 
                raise IndexError(f"Cannot index list with {type(name)}")
            return self.__value__[name]
        raise RuntimeError
        
    def __setitem__(self, name, value):
        if self.__nodetype__ == "null":
            if isinstance(name, int):
                raise IndexError("list assignment index out of range")
            self.__value__ = {}
        if self.__nodetype__ == "dict": 
            if name not in self.__value__: 
                self.__value__[name] = Tree(value)
            return
        if self.__nodetype__ == "list": 
            if not isinstance(name, int): 
                raise IndexError(f"Cannot index list with {type(name)}")
            self.__value__[name] = Tree(value)
            return
        raise RuntimeError

    def __iter__(self):
        return iter(self.__value__)

    def __len__(self):
        return len(self.__value__)

    def __contains__(self, value):
        return self.__value__.__contains__(value)
        
    def append(self, *args, **kwargs):
        """
        Appends a value to a list node (tree branch). If the node type was previously undefined, the node becomes a list. 

        Note
        ---------
        The append method can take either one positional argument or one-to-many named (keyword) arguments. If passed one-to-many keyword arguments, the kwargs dictionary is added to the list.

        Example
        ---------
        >>> tree = easytree.new()                                 #undefined node
        >>> tree.append("hello world")                            #casts node to list
        >>> tree.append(name="David", age=29)                     #call with kwargs
        >>> tree.append({"animal":"elephant", "country":"India"}) #call with args
        >>> easytree.serialize(tree)
        ["Hello world",{"name":"David","age":29},{"animal":"elephant", "country":"India"}]

        """
        if len(args) > 1 or (len(args) != 0 and len(kwargs) != 0) or (len(args) == len(kwargs) == 0): 
            raise ValueError("append must take either one positional argument or one-to-many named arguments")
        value = args[0] if args else kwargs
        if self.__nodetype__ == "null":
            self.__value__ = []        
        if self.__nodetype__ == "list":
            if isinstance(value, (list, tuple, set)):
                value = [Tree(v) for v in value]
            elif isinstance(value, dict):
                value = Tree({k:Tree(v) for k,v in value.items()})
            else:
                value = Tree(value)
            return self.__value__.append(value)
        raise RuntimeError

    def serialize(self):
        """
        Recursively converts itself to a native python type.

        Example
        ---------------------
        >>> chart = easytree.new()
        >>> chart.chart.type = "bar"
        >>> chart.title.text = "France Olympic Medals"
        >>> chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
        >>> chart.yAxis.title.text = "Count"
        >>> chart.series.append(name="2016", data=[10, 18, 14])
        >>> chart.series.append({"name":"2012", "data":[11,11,13]})
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
        """
        return serialize(self)
    
def serialize(tree):
    """
    Recursively converts an :code:`easytree.Tree` to a native python type.

    Example
    ---------------------
    >>> chart = easytree.new()
    >>> chart.chart.type = "bar"
    >>> chart.title.text = "France Olympic Medals"
    >>> chart.xAxis.categories = ["Gold", "Silver", "Bronze"]
    >>> chart.yAxis.title.text = "Count"
    >>> chart.series.append(name="2016", data=[10, 18, 14])
    >>> chart.series.append({"name":"2012", "data":[11,11,13]})
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
    """
    if not isinstance(tree, Tree):
        return tree
    if tree.__nodetype__ == "null":
        return None
    if tree.__nodetype__ == "list":
        return [serialize(value) for value in tree.__value__]
    if tree.__nodetype__ == "dict":
        return {key:serialize(value) for key, value in tree.__value__.items()}
    raise RuntimeError


def new(root=None): 
    """
    Creates an :code:`easytree.Tree`
    """
    return Tree(root)