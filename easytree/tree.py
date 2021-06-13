import json
import collections.abc as abc


class AmbiguityError(Exception):
    pass


class NODETYPES:
    DICT = "dict"
    LIST = "list"
    UNDEFINED = "undefined"


class Node:
    __hash__ = None

    def __new__(cls, value=None, *args, **kwargs):
        if cls is not Node:
            return super().__new__(cls)
        if value is None or isinstance(
            value,
            (list, tuple, set, range, zip, dict, Node, abc.KeysView, abc.ValuesView),
        ):
            return super().__new__(cls)
        return value

    def __init__(self, value=None, *, sealed=False, frozen=False):
        if isinstance(value, Node):
            value = value.serialize()
        if isinstance(value, dict):
            value = {k: Node(v, sealed=sealed, frozen=frozen) for k, v in value.items()}
        elif isinstance(
            value, (list, tuple, set, range, zip, abc.KeysView, abc.ValuesView)
        ):
            value = [Node(v, sealed=sealed, frozen=frozen) for v in value]
        elif value is not None:
            raise TypeError(
                "tree node must be initialized with either None, dict, or list"
            )
        self._value = value
        self._frozen = frozen
        self._sealed = sealed

    def __repr__(self):
        return repr(serialize(self))

    def __str__(self):
        return str(serialize(self))

    @property
    def __nodetype(self):
        """
        Returns the type of the node
        """
        if "_value" not in self.__dict__ or self._value is None:
            return NODETYPES.UNDEFINED
        if isinstance(self._value, list):
            return NODETYPES.LIST
        if isinstance(self._value, dict):
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
            return True  # ipython workaround
        if name in ("_frozen", "_sealed"):
            return False  # defaults for inheritence
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError(f"list node has not attribute '{name}'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            if self._frozen:
                raise AttributeError(f"frozen node does not have '{name}' attribute")
            if self._sealed:
                raise AttributeError(f"sealed node does not have '{name}' attribute")
            self._value = {}
        if name not in self._value:
            if self._frozen:
                raise AttributeError(f"frozen node does not have '{name}' attribute")
            if self._sealed:
                raise AttributeError(f"sealed node does not have '{name}' attribute")
            self._value[name] = Node(sealed=self._sealed, frozen=self._frozen)
        return self._value[name]

    def __setattr__(self, name, value):
        """
        Sets the value at an attribute for dict nodes. 

        If the node is undefined, this operation casts the node to 
        a dict node.

        Raises an AttributeError for list nodes. 
        """
        if name in ("_value", "_frozen", "_sealed"):
            return super().__setattr__(name, value)
        if name in {"serialize", "get", "append"}:
            raise AttributeError(f"Attribute '{name}' is read-only")
        if self.__nodetype == NODETYPES.UNDEFINED:
            if self._frozen:
                raise AttributeError(
                    f"cannot set new attribute '{name}' on frozen node"
                )
            if self._sealed:
                raise AttributeError(
                    f"cannot set new attribute '{name}' on sealed node"
                )
            self._value = {}
        if self.__nodetype == NODETYPES.DICT:
            if self._frozen:
                raise AttributeError(f"cannot set attribute '{name}' on frozen node")
            if name not in self._value and self._sealed:
                raise AttributeError(
                    f"cannot set new attribute '{name}' on sealed node"
                )
            self._value[name] = Node(value, sealed=self._sealed, frozen=self._frozen)
            return
        raise AttributeError(f"list node has not attribute '{name}'")

    def __delattr__(self, name):
        """
        Remove an attribute by name
        """
        if name in {
            "__nodetype",
            "_value",
            "_frozen",
            "_sealed",
            "serialize",
            "get",
            "append",
        }:
            raise AttributeError(f"Attribute '{name}' is read-only")
        if self.__nodetype == NODETYPES.UNDEFINED:
            raise AttributeError(f"undefined node has no attribute '{name}'")
        if self._frozen:
            raise AttributeError(f"cannot delete attribute '{name}' on frozen node")
        if self._sealed:
            raise AttributeError(f"cannot delete attribute '{name}' on sealed node")
        del self._value[name]

    def __getitem__(self, name):
        """
        Retrieves an item at an index (for list nodes) or at a key (for dict nodes). 

        If the node is undefined, this operation casts the node to a dict node, 
        unless the given key/index is an integer; instead, an AmbiguityError error is 
        raised.
        """
        if self.__nodetype == NODETYPES.UNDEFINED:
            if self._frozen:
                raise KeyError(f"frozen node has no value for '{name}'")
            if self._sealed:
                raise KeyError(f"sealed node has no value for '{name}'")
            if isinstance(name, (int, slice)):
                raise AmbiguityError(
                    "Node type is undefined: cast to dict node or list node to disambiguate"
                )
            else:
                self._value = {}
        if self.__nodetype == NODETYPES.DICT:
            if name not in self._value:
                if self._frozen:
                    raise KeyError(f"frozen node has no value for '{name}'")
                if self._sealed:
                    raise KeyError(f"sealed node has no value for '{name}'")
                self._value[name] = Node(sealed=self._sealed, frozen=self._frozen)
            return self._value[name]
        if self.__nodetype == NODETYPES.LIST:
            if not isinstance(name, (int, slice)):
                raise TypeError(
                    f"list indices must be integers or slices, not {type(name).__name__}"
                )
            return self._value[name]
        raise RuntimeError

    def __setitem__(self, name, value):
        """
        Sets the value at an index (for list nodes) or at a key (for dict node). 

        If the node is undefined, this operation casts the node to a dict node, 
        unlesss the given key/index is a slice object. 
        """
        if self._frozen:
            raise TypeError(f"cannot set item '{name}' on frozen node")
        if self.__nodetype == NODETYPES.UNDEFINED:
            if isinstance(name, int):
                raise IndexError("list assignment index out of range")
            elif isinstance(name, slice):
                self._value = []
            else:
                self._value = {}
        if self.__nodetype == NODETYPES.DICT:
            if name not in self._value and self._sealed:
                raise TypeError(f"cannot set new item '{name}' on sealed node")
            self._value[name] = Node(value, sealed=self._sealed, frozen=self._frozen)
            return
        if self.__nodetype == NODETYPES.LIST:
            if not isinstance(name, (int, slice)):
                raise TypeError(f"cannot index list with {type(name)}")
            self._value[name] = Node(value, sealed=self._sealed, frozen=self._frozen)
            return
        raise RuntimeError

    def __delitem__(self, name):
        """
        Deletes the value at an index (for list nodes) or at a key (for dict node). 
        """
        if self._frozen:
            raise TypeError(f"cannot delete item '{name}' on frozen node")
        if self._sealed:
            raise TypeError(f"cannot delete item '{name}' on sealed node")
        if self.__nodetype == NODETYPES.UNDEFINED:
            raise AttributeError("undefined node has no attribute '{name}'")
        del self._value[name]

    def __iter__(self):
        """
        Iterates over the underlying value.
        """
        if self.__nodetype == NODETYPES.UNDEFINED:
            raise TypeError("undefined node is not iterable")
        return iter(self._value)

    def __len__(self):
        """
        Returns the length of the underlying value.
        """
        if self.__nodetype == NODETYPES.UNDEFINED:
            raise TypeError("undefined node has no length")
        return len(self._value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def __contains__(self, value):
        if self.__nodetype == NODETYPES.UNDEFINED:
            raise TypeError("undefined node is not iterable")
        return self._value.__contains__(value)

    def __bool__(self):
        return bool(self._value)

    def append(self, *args, **kwargs):
        """
        Appends a value to a list node. If the node type was previously undefined, the node becomes a list. 

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
        if self._frozen or self._sealed:
            raise TypeError("cannot append value to frozen or sealed node")
        if (
            len(args) > 1
            or (len(args) != 0 and len(kwargs) != 0)
            or (len(args) == len(kwargs) == 0)
        ):
            raise ValueError(
                "append must take either one positional argument or one-to-many named arguments"
            )
        value = args[0] if args else kwargs
        if self.__nodetype == NODETYPES.UNDEFINED:
            self._value = []
        if self.__nodetype == NODETYPES.LIST:
            value = Node(value, sealed=self._sealed, frozen=self._frozen)
            self._value.append(value)
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
        2016-03-31
        >>> config.context.get("ending", "2021-12-31")
        2021-12-31
        >>> config.context.get("calendar")
        None
        """
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError("list node has no attribute 'get'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            return default
        if key in self._value:
            return self._value[key]
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
    if not isinstance(tree, Node):
        return tree
    if tree._Node__nodetype == NODETYPES.UNDEFINED:
        return None
    if tree._Node__nodetype == NODETYPES.LIST:
        return [serialize(value) for value in tree._value]
    if tree._Node__nodetype == NODETYPES.DICT:
        return {key: serialize(value) for key, value in tree._value.items()}
    raise RuntimeError


def new(root=None, *, sealed=False, frozen=False):
    """
    Creates a new :code:`easytree.Tree`
    """
    return Node(root, sealed=sealed, frozen=frozen)


def load(stream, *args, frozen=False, sealed=False, **kwargs):
    """
    Deserialize a text file or binary file containing a JSON 
    document to an easytree.Tree object 

    Example
    -------------
    >>> with open("data.json", "r") as file: 
    ...     tree = easytree.load(file)
    """
    return Node(json.load(stream, *args, **kwargs), sealed=sealed, frozen=frozen)


def loads(s, *args, frozen=False, sealed=False, **kwargs):
    """
    Deserialize s (a str, bytes or bytearray instance containing a JSON document) 
    to an easytree.Node object 
    """
    return Node(json.loads(s, *args, **kwargs), sealed=sealed, frozen=frozen)


def dump(obj, stream, *args, **kwargs):
    """
    Serialize easytree.Tree object as a JSON formatted string 
    to stream (a .write()-supporting file-like object)

    Example
    -------------
    >>> tree = easytree.Tree({"foo": "bar"})
    >>> with open("data.json", "w") as file: 
    ...     easytree.dump(tree, file, indent=4)
    """
    return json.dump(serialize(obj), stream, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    """
    Serialize easytree.Tree to a JSON formatted string
    """
    return json.dumps(serialize(obj), *args, **kwargs)


def frozen(tree):
    """
    Returns True if the tree is frozen
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return tree._frozen


def freeze(tree):
    """
    Returns a new frozen copy of the tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, frozen=True)


def unfreeze(tree):
    """
    Returns a new unfrozen copy of the tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, frozen=False)


def sealed(tree):
    """
    Returns True if the tree is sealed
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return tree._frozen


def seal(tree):
    """
    Returns a new sealed copy of the tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, sealed=False)


def unseal(tree):
    """
    Returns a new unsealed copy of the tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, sealed=False)
