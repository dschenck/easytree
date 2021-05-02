class AmbiguityError(Exception):
    pass

class NODETYPES: 
    DICT = "dict"
    LIST = "list"
    UNDEFINED = "undefined"

class Tree:
    def __init__(self, value=None):
        if isinstance(value, Tree):
            value = value.serialize()
        if isinstance(value, dict):
            value = {k:Node(v) for k,v in value.items()}
        elif isinstance(value, (list, tuple, set, range, zip)):
            value = [Node(v) for v in value]
        elif isinstance(value, Node):
            value = value.__value__
        elif value is not None: 
            raise TypeError("tree must be initialized with either None, dict, or list")
        self.__value__ = value

    def __repr__(self):
        return repr(serialize(self))
    
    def __str__(self):
        return str(serialize(self))
        
    @property
    def __nodetype__(self):
        """
        Returns the type of the node
        """
        if "__value__" not in self.__dict__ or self.__value__ is None: 
            return NODETYPES.UNDEFINED
        if isinstance(self.__value__, list):
            return NODETYPES.LIST
        if isinstance(self.__value__, dict):
            return NODETYPES.DICT
        raise RuntimeError
    
    def __getattr__(self, name):
        """
        Retrieves an attribute by name for dict nodes.

        If the node is undefined, this operations casts the node to
        a dict node.

        Raises an AttributeError for list nodes. 
        """
        if name == "_ipython_canary_method_should_not_exist_":
            return True #ipython workaround
        if self.__nodetype__ == NODETYPES.LIST:
            raise AttributeError(f"list node has not attribute '{name}'")
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            self.__value__ = {}
        if name not in self.__value__:
            self.__value__[name] = Node()
        return self.__value__[name]
    
    def __setattr__(self, name, value):
        """
        Sets the value at an attribute for dict nodes. 

        If the node is undefined, this operation casts the node to 
        a dict node.

        Raises an AttributeError for list nodes. 
        """
        if name == "__value__":
            return super().__setattr__(name, value)
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            self.__value__ = {}
        if self.__nodetype__ == NODETYPES.DICT: 
            self.__value__[name] = Node(value)
            return
        raise AttributeError(f"list node has not attribute '{name}'")
    
    def __delattr__(self, name):
        """
        Remove an attribute by name
        """
        if name in {"__nodetype__", "__value__", "serialize"}: 
            raise AttributeError(f"Attribute '{name}' is read-only")
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            raise AttributeError("undefined node has no attribute '{name}'")
        del self.__value__[name]
        
    def __getitem__(self, name):
        """
        Retrieves an item at an index (for list nodes) or at a key (for dict nodes). 

        If the node is undefined, this operation casts the node to a dict node, 
        unless the given key/index is an integer; instead, an AmbiguityError error is 
        raised.
        """
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            if isinstance(name, (int, slice)): 
                raise AmbiguityError("Node type is undefined: cast to dict node or list node to disambiguate")
            else:
                self.__value__ = {}
        if self.__nodetype__ == NODETYPES.DICT: 
            if name not in self.__value__: 
                self.__value__[name] = Node()
            return self.__value__[name]
        if self.__nodetype__ == NODETYPES.LIST: 
            if not isinstance(name, (int, slice)): 
                raise TypeError(f"list indices must be integers or slices, not {type(name).__name__}")
            return self.__value__[name]
        raise RuntimeError
        
    def __setitem__(self, name, value):
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            if isinstance(name, int):
                raise IndexError("list assignment index out of range")
            elif isinstance(name, slice):
                self.__value__ = []
            else:
                self.__value__ = {}
        if self.__nodetype__ == NODETYPES.DICT: 
            self.__value__[name] = Node(value)
            return
        if self.__nodetype__ == NODETYPES.LIST: 
            if not isinstance(name, int): 
                raise IndexError(f"Cannot index list with {type(name)}")
            self.__value__[name] = Node(value)
            return
        raise RuntimeError

    def __delitem__(self, name):
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            raise AttributeError("undefined node has no attribute '{name}'")
        del self.__value__[name]

    def __iter__(self):
        return iter(self.__value__)

    def __len__(self):
        return len(self.__value__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def __contains__(self, value):
        return self.__value__.__contains__(value)

    def __bool__(self):
        return bool(self.__value__)
        
    def append(self, *args, **kwargs):
        """
        Appends a value to a list node (tree branch). If the node type was previously undefined, the node becomes a list. 

        Note
        ---------
        The append method can take either one positional argument or one-to-many named (keyword) arguments. If passed one-to-many keyword arguments, the kwargs dictionary is added to the list.

        Example
        ---------
        >>> tree = easytree.Tree()                                 #undefined node
        >>> tree.append("hello world")                            #casts node to list
        >>> tree.append(name="David", age=29)                     #call with kwargs
        >>> tree.append({"animal":"elephant", "country":"India"}) #call with args
        >>> easytree.serialize(tree)
        ["Hello world",{"name":"David","age":29},{"animal":"elephant", "country":"India"}]

        Note
        ---------
        The append method intentionally returns a reference to the last-added item, if that item is a new node. This allows for more fluent code using the context manager. 

        Example
        -----------
        >>> chart = easytree.Tree()
        >>> with chart.axes.append({}) as axis: 
        ...     axis.title.text = "primary axis"
        >>> with chart.axes.append({}) as axis: 
        ...     axis.title.text = "secondary axis"
        >>> chart.serialize()
        {
            "axes": [
                {
                    "title": {
                        "text": "primary axis"
                    }
                },
                {
                    "title": {
                        "text": "secondary axis"
                    }
                }
            ]
        }
        """
        if len(args) > 1 or (len(args) != 0 and len(kwargs) != 0) or (len(args) == len(kwargs) == 0): 
            raise ValueError("append must take either one positional argument or one-to-many named arguments")
        value = args[0] if args else kwargs
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            self.__value__ = []        
        if self.__nodetype__ == NODETYPES.LIST:
            value = Node(value)
            self.__value__.append(value)
            return value if isinstance(value, Node) else None 
        raise AttributeError("dict node has no attribute 'append'")

    def get(self, key, default=None):
        """
        Returns the value at a given key, or default if the key does 
        not exists.

        Example
        ---------------------
        >>> config = easytree.Tree({"context":{"starting":"2016-03-31"}})
        >>> config.context.get("starting", "2014-01-01")
        2014-01-01
        >>> config.context.get("ending", "2021-12-31")
        2021-12-31
        >>> config.context.get("calendar")
        None
        """
        if self.__nodetype__ == NODETYPES.LIST:
            raise AttributeError("list node has no attribute 'get'")
        if self.__nodetype__ == NODETYPES.UNDEFINED:
            return default
        if key in self.__value__: 
            return self.__value__[key]
        return default

    def serialize(self):
        """
        Recursively converts itself to a native python type (dict, list or None).

        Example
        ---------------------
        >>> chart = easytree.Tree()
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

class Node(Tree):
    """
    Tree node
    """
    __hash__ = None 
    
    def __new__(cls, value=None):
        if cls is not Node: 
            return super(cls, cls).__new__(cls)
        if value is None or isinstance(value, (list, tuple, set, range, zip, dict)):
            return super(Node, cls).__new__(cls)
        return value

    def __repr__(self):
        return f"<Node type={self.__nodetype__}>"
    
def serialize(tree):
    """
    Recursively converts an :code:`easytree.Tree` to a native python type.

    Example
    ---------------------
    >>> chart = easytree.Tree()
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
    if tree.__nodetype__ == NODETYPES.UNDEFINED:
        return None
    if tree.__nodetype__ == NODETYPES.LIST:
        return [serialize(value) for value in tree.__value__]
    if tree.__nodetype__ == NODETYPES.DICT:
        return {key:serialize(value) for key, value in tree.__value__.items()}
    raise RuntimeError

def new(root=None): 
    """
    Creates a new :code:`easytree.Tree`
    """
    return Tree(root)