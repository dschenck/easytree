import collections.abc as abc
import warnings


class NODETYPES:
    DICT = "dict"
    LIST = "list"
    UNDEFINED = "undefined"


class Node:
    """
    .. attention:: This class is deprecated since 0.2.0 and may be removed in future versions. Use :code:`easytree.dict` or :code:`easytree.list` instead.

    A recursive tree structure, supporting both dict and list nodes. New children nodes can be read and written as attributes, and dynamically become nodes themselves.

    Example
    -------------
    >>> root = easytree.Tree()
    >>> root.user.firstname = "foo"
    >>> root.user.firstname == root["user"]["firstname"] == "foo"
    True
    >>> root.user.friends.append(username="@jack")
    >>> root
    {
        "user":{
            "firstname":"foo"
        },
        "friends":[
            {
                "username":"@jack"
            }
        ]
    }

    The type of a newly-accessed node is initially *undefined*, but is cast as a dict or a list depending on subsequent interactions.

    Example
    ------------
    >>> root = easytree.Tree()
    >>> root.abc                              #abc is an undefined node
    >>> root.abc.xyz                          #abc is cast to a dict node; xyz is undefined
    >>> root.abc.xyz.append(firstname="Bob")  #xyz is cast to a list node with one dict node

    A tree can be *serialized* back to native python objects using the :code:`serialize` method

    Example
    -------------
    >>> tree = easytree.Tree()
    >>> tree.abc.xyz.append(44)
    >>> tree.serialize()
    {
        "abc":{
            "xyz:[
                44
            ]
        }
    }

    A tree can be *sealed* or *frozen* to prevent further changes

    Example
    --------------
    >>> tree = easytree.Tree({"abc":{"xyz":True}}, sealed=True)
    >>> tree.abc.xyz = False
    >>> tree.foo = "bar"
    AttributeError: cannot set new attribute 'foo' on sealed node
    """

    __hash__ = None

    def __new__(cls, value=None, *args, **kwargs):
        if cls is not Node:
            return super().__new__(cls)
        if value is None or isinstance(
            value, (list, tuple, set, range, zip, dict, abc.KeysView, abc.ValuesView)
        ):
            return super().__new__(cls)
        # keep subclass instances intact
        if isinstance(value, Node) and type(value) is Node:
            return super().__new__(cls)
        return value

    def __init__(self, value=None, *, sealed=False, frozen=False):
        warnings.warn(
            "easytree.Tree will be deprecated in future versions. Use :code:`easytree.dict` or :code:`easytree.list` instead",
            DeprecationWarning,
            stacklevel=2,
        )

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
        return f"Tree({repr(serialize(self))})"

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

        If the node is undefined, this operations casts the node to a dict node.

        Raises an AttributeError for list nodes.
        """
        if name == "_ipython_canary_method_should_not_exist_":
            return True  # ipython workaround
        if name in ("_frozen", "_sealed"):
            return False  # defaults for inheritence
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError(f"list node has no attribute '{name}'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            if self._frozen:
                raise AttributeError(f"frozen node has no attribute '{name}'")
            if self._sealed:
                raise AttributeError(f"sealed node has no attribute '{name}'")
            self._value = {}
        if name not in self._value:
            if self._frozen:
                raise AttributeError(f"frozen node has no attribute '{name}'")
            if self._sealed:
                raise AttributeError(f"sealed node has no attribute '{name}'")
            self._value[name] = Node(sealed=self._sealed, frozen=self._frozen)
        return self._value[name]

    def __setattr__(self, name, value):
        """
        Sets the value at an attribute for dict nodes.

        If the node is undefined, this operation casts the node to a dict node.

        Raises an AttributeError for list nodes.
        """
        if name in ("_value", "_frozen", "_sealed"):
            return super().__setattr__(name, value)
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
        raise AttributeError(f"list node has no attribute '{name}'")

    def __delattr__(self, name):
        """
        Remove an attribute by name
        """
        if name in {"__nodetype", "_value", "_frozen", "_sealed"}:
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

        If the node is undefined, this operation casts the node to a dict node.
        """
        if self.__nodetype == NODETYPES.UNDEFINED:
            if self._frozen:
                raise KeyError(f"frozen node has no value for '{name}'")
            if self._sealed:
                raise KeyError(f"sealed node has no value for '{name}'")
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

        If the node is undefined, this operation casts the node to a dict node, unlesss the given key/index is a slice object.
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

    def __getstate__(self):
        """
        Returns the state of the tree for pickling
        """
        return self.__dict__

    def __setstate__(self, data):
        """
        Unpickles and restores the state of the tree
        """
        self.__dict__.update(data)

    def append(self, *args, **kwargs):
        """
        Appends a value to a list node. If the node type was previously undefined, the node becomes a list.

        Note
        ---------
        The append method can take either one positional argument or one-to-many named (keyword) arguments. If passed one-to-many keyword arguments, the kwargs dictionary is added to the list.

        Examples
        ---------
        >>> tree = easytree.Tree()                                 #undefined node
        >>> tree.append("hello world")                            #casts node to list
        >>> tree.append(name="David", age=29)                     #call with kwargs
        >>> tree.append({"animal":"elephant", "country":"India"}) #call with args
        >>> tree.serialize()
        ["Hello world",{"name":"David","age":29},{"animal":"elephant", "country":"India"}]

        Note
        ---------
        The append method intentionally returns a reference to the last-added item, if that item is a new node. This allows for fluent code using the context manager.

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
        Returns the value at a given key, or default if the key does not exists.

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

    def deepget(self, keys, default=None):
        """
        Returns the value at the end of the keys' path, or
        default if such path raises an KeyError or IndexError

        Parameters
        ----------
        keys : iterable
            list of keys
        default : *
            default value if keys' path does not exists

        Example
        -------
        >>> tree = easytree.Tree({"address":{"city":"New York"}})
        >>> tree.deepget(("address","city"))
        "New York"
        >>> tree.deepget(("address","country"), "US")
        "US"
        """
        node = self
        for key in keys:
            if isinstance(node, Node):
                if node._Node__nodetype == NODETYPES.UNDEFINED:
                    return default
                if node._Node__nodetype == NODETYPES.DICT:
                    if key not in node:
                        return default
            try:
                node = node[key]
            except (KeyError, IndexError):
                return default
        return node

    def pop(self, *args, **kwargs):
        """
        Removes (in-place) the item at given key/index and returns the corresponding value.

        Note
        ----
        Calling pop on an undefined node

        Example
        -------
        >>> tree = easytree.Tree({"name":"Bob","numbers":[1,3,5], "address":{"country":"US"}})
        >>> tree.pop("name")
        "Bob"
        >>> tree
        easytree.Tree({"numbers":[1,3,5], "address":{"country":"US"}})
        >>> tree.numbers.pop()
        5
        >>> tree
        easytree.Tree({"numbers":[1,3], "address":{"country":"US"}})
        """
        if self.__nodetype == NODETYPES.UNDEFINED:
            if len(args) + len(kwargs) == 2:
                return {}.pop(*args, **kwargs)
            if len(args) + len(kwargs) == 0:
                return [].pop()
            if len(args) == 0 and len(kwargs) == 1 and "index" in kwargs:
                return [].pop(**kwargs)
            return {}.pop(*args, **kwargs)
        return self._value.pop(*args, **kwargs)

    def keys(self):
        """
        Returns the keys at the dict node

        Returns
        -------
        dict_keys

        Raises
        ------
        AttributeError
            if node is a list node
        """
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError("list node has no attribute 'keys'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            return {}.keys()
        return self._value.keys()

    def values(self):
        """
        Returns the values at the dict node

        Returns
        -------
        dict_values

        Raises
        ------
        AttributeError
            if node is a list node
        """
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError("list node has no attribute 'values'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            return {}.values()
        return self._value.values()

    def items(self):
        """
        Returns the items at the dict node

        Returns
        -------
        dict_items

        Raises
        ------
        AttributeError
            if node is a list node
        """
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError("list node has no attribute 'items'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            return {}.items()
        return self._value.items()

    def update(self, other):
        """
        Updates (in place) the dict node with other mapping

        Note
        ----
        An undefined node will be cast as a dict node

        Returns
        -------
        None

        Raises
        ------
        AttributeError
            if node is a list node
        """
        if self.__nodetype == NODETYPES.LIST:
            raise AttributeError("list node has no attribute 'items'")
        if self.__nodetype == NODETYPES.UNDEFINED:
            self._value = Node(other)._value
        else:
            self._value.update(Node(other)._value)
        return

    def serialize(self):
        """
        .. attention:: Deprecated since 0.2.0

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


def serialize(tree: Node):
    """
    .. attention:: Deprecated since 0.2.0

    Recursively converts an :code:`easytree.Tree` back to a native python type.

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