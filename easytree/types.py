import builtins
import easytree


def cast(value, *, sealed=False, frozen=False):
    """
    Convert a value to an easytree object, when possible, based on its type.

    - dict instances are cast to easytree.dict instances.
    - lists instances are cast to easytree.list instances
    - other types are returns as is, without further transformations

    Parameters
    ----------
    value : any
        the value to cast to an easytree type
    sealed : bool
        True if cast object is sealed, False otherwise
    frozen : bool
        True if cast object is frozen, False otherwise

    Returns
    -------
    cast : any
        the cast value, or value itself, as the case may be
    """
    if isinstance(value, (list, dict)):
        if (easytree.sealed(value) is sealed) and (easytree.frozen(value) is frozen):
            return value
        # version 0.2.1 - allow for subclassing of easytree.dict and easytree.list
        return type(value)(value, sealed=sealed, frozen=frozen)
    if isinstance(value, builtins.dict):
        return dict(value, sealed=sealed, frozen=frozen)
    if isinstance(value, builtins.list):
        return list(value, sealed=sealed, frozen=frozen)
    if isinstance(value, tuple):
        return tuple(cast(x, sealed=sealed, frozen=frozen) for x in value)
    if isinstance(value, set):
        return {cast(x, sealed=sealed, frozen=frozen) for x in value}
    return value


class list(builtins.list):
    """
    easytree.list

    Parameters
    ----------
    args : iterable, None
        an iterable values

    sealed : bool
        True if list is sealed, False otherwise

    frozen : bool
        True if list is frozen, False otherwise

    Note
    ----
    Lists and dicts included or appended in the list
    are recursively sealed and frozen as per its containing parent.
    """

    def __init__(self, args=None, *, sealed=False, frozen=False):
        super().__init__(
            [cast(arg, sealed=sealed, frozen=frozen) for arg in (args or [])]
        )
        self._sealed = sealed
        self._frozen = frozen

    def __setitem__(self, key, value):
        """
        Set a value in the list at an index or slice

        If the value is a list or a dict, the value is cast to
        an :code:`easytree.list` or :code:`easytree.dict`

        Parameters
        ----------
        key : int, slice
            the index or slice of indices
        value : any
            the value

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot set item on frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot set item on sealed easytree.list")
        return super().__setitem__(
            key, cast(value, frozen=self._frozen, sealed=self._sealed)
        )

    def __delitem__(self, key):
        """
        Delete an item from the list by its index

        Parameter
        ---------
        key : int, slice
            the index or slice of indices

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot delete item from frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot delete item from sealed easytree.list")
        return super().__delitem__(key)

    def __enter__(self):
        """
        For convenience, you can use a context manager to write to deeply
        nested trees.

        The context manager has no side effect.

        Returns
        -------
        self : list
            the list itself
        """
        return self

    def __exit__(self, *args, **kwargs):
        """
        Exit the context manager
        """
        pass

    def __reduce__(self):
        """
        Pickling reducer
        """
        return self.__class__, (), self.__dict__, iter(self), None

    def __setstate__(self, state):
        """
        Pickling setter
        """
        self.__dict__.update(state)

    def append(self, *args, **kwargs):
        """
        Append a value to the list

        Note
        ---------
        The :code:`append` method can take either one positional argument or
        one-to-many named (keyword) arguments. If passed keyword
        arguments, the kwargs dictionary is added to the list as an
        :code:`easytree.dict`.

        Returns
        -------
        item : any
            the last added item

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        ValueError
            if neither a value nor a set of kwargs is given

        Example
        -------
        >>> tree = easytree.list()                                # list node
        >>> tree.append("hello world")                            # simple append
        >>> tree.append(name="David", age=29)                     # call with kwargs
        >>> tree.append({"animal":"elephant", "country":"India"}) # call with dict
        >>> tree
        [
            "Hello world",
            {
                "name": "David",
                "age": 29
            },
            {
                "animal": "elephant",
                "country": "India"
            }
        ]

        Note
        ---------
        The append method intentionally returns a reference to the last-added item. This allows for fluent code using the context manager.

        Example
        -------
        >>> chart = easytree.dict()
        >>> with chart.axes.append({}) as axis:
        ...     axis.title.text = "primary axis"
        >>> with chart.axes.append({}) as axis:
        ...     axis.title.text = "secondary axis"
        >>> chart
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
        if self._frozen:
            raise TypeError("cannot append value to frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot append value to sealed easytree.list")
        if (
            len(args) > 1
            or (len(args) != 0 and len(kwargs) != 0)
            or (len(args) == len(kwargs) == 0)
        ):
            raise ValueError(
                "append must take either one positional argument or one-to-many named arguments"
            )

        super().append(
            cast(args[0] if args else kwargs, sealed=self._sealed, frozen=self._frozen)
        )
        return self[len(self) - 1]

    def extend(self, other):
        """
        Extend the list by appending all the items from another iterable.

        list or dict items from other are cast to :code:`easytree.list` or
        :code:`easytree.dict` values respectively.

        Parameters
        ----------
        other : iterable
            the other iterable

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot extend frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot extend sealed easytree.list")
        return super().extend(
            [cast(v, sealed=self._sealed, frozen=self._frozen) for v in other]
        )

    def insert(self, index, value):
        """
        Insert an item into the list at a given position.

        If the value is a list or a dict, the value is cast to
        an :code:`easytree.list` or :code:`easytree.dict`

        Parameters
        ----------
        index : int
            the index at which to insert the value
        value : any
            the inserted value

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot insert into frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot insert into sealed easytree.list")
        return super().insert(
            index, cast(value, sealed=self._sealed, frozen=self._frozen)
        )

    def remove(self, x):
        """
        Remove the first item from the list whose value is equal to x.

        Parameters
        ----------
        x : any
            the value to remove

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        ValueError
            if there is no such item
        """
        if self._frozen:
            raise TypeError("cannot remove from frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot remove from sealed easytree.list")
        return super().remove(x)

    def pop(self, *args):
        """
        Remove the item at the given position in the list,
        and return it.

        Returns
        -------
        item : any
            the popped item

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot pop from frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot pop from sealed easytree.list")
        return super().pop(*args)

    def clear(self):
        """
        Remove all items from the list.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot clear frozen easytree.list")
        if self._sealed:
            raise TypeError("cannot clear sealed easytree.list")
        return super().clear()

    def sort(self, *, key=None, reverse=False):
        """
        Sort the items of the list in place

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is frozen
        """
        if self._frozen:
            raise TypeError("cannot sort frozen easytree.list")
        return super().sort(key=key, reverse=reverse)

    def reverse(self):
        """
        Reverse the elements of the list in place.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        if self._frozen:
            raise TypeError("cannot reverse frozen easytree.list")
        return super().reverse()

    def copy(self):
        """
        Return a shallow copy of the list

        Returns
        -------
        copy : list
            the new list
        """
        return list(self, frozen=self._frozen, sealed=self._sealed)


class dict(builtins.dict):
    """
    recursive dot-styled defaultdict
    """

    def __init__(self, *args, sealed=False, frozen=False, **kwargs):
        super().__init__(
            {
                k: cast(v, sealed=sealed, frozen=frozen)
                for k, v in builtins.dict(*args, **kwargs).items()
            }
        )
        self._sealed = sealed
        self._frozen = frozen

    def __getitem__(self, key):
        """
        Returns a value at a key, or :code:`undefined` if
        key does not exist

        Raises
        ------
        KeyError
            if the dict is frozen or sealed, and the key does not
            exist in the dict
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            if self._frozen:
                raise KeyError(f"frozen easytree.dict has no value for {key}") from None
            if self._sealed:
                raise KeyError(f"sealed easytree.dict has no value for {key}") from None
        return undefined(parent=self, key=key)

    def __setitem__(self, key, value):
        """
        Set a value at a key

        Returns
        -------
        None

        Raises
        ------
        KeyError
            if the dict is frozen, or if the dict is sealed and the key does not exist in the dict
        """
        if self._frozen:
            raise KeyError(f"cannot define value for {key} on frozen easytree.dict")
        if self._sealed and key not in self:
            raise KeyError(f"sealed define value for {key} on sealed easytree.dict")
        super().__setitem__(key, value)

    def __getattr__(self, key):
        """
        Returns a value at a key, or :code:`undefined` if
        key does not exist

        Note
        ----
        if key is :code:`_frozen` or :code:`_sealed`,
        then the instance is an instance of a subclass
        to :code:`easytree.dict` which overrode the
        default :code:`__init__`

        Raises
        ------
        AttributeError
            if the dict is frozen and the key does not exist in the dict, or
            if the dict is sealed and the key does not exist in the dict
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            if key in ["_frozen", "_sealed"]:
                return False  # if subclass overrides the init (see note)
            if self._frozen:
                raise AttributeError(
                    f"frozen easytree.dict has no attribute {key}"
                ) from None
            if self._sealed:
                raise AttributeError(
                    f"sealed easytree.dict has no attribute {key}"
                ) from None
        return undefined(parent=self, key=key)

    def __setattr__(self, key, value):
        """
        Sets a value at a key, recursively casting the value
        to a :code:`easytree.dict` or :code:`easytree.list`.

        Raises
        ------
        AttributeError
            if the dict is frozen, or if the dict is sealed and the key does not exist in the dict
        """
        if key in ["_sealed", "_frozen"]:
            return super().__setattr__(key, value)
        if self._frozen:
            raise AttributeError(f"cannot set attribute {key} on frozen easytree.dict")
        if self._sealed and key not in self:
            raise AttributeError(
                f"cannot define attribute {key} on sealed easytree.dict"
            )
        self[key] = cast(value, sealed=self._sealed, frozen=self._frozen)

    def __delattr__(self, key: str) -> None:
        """
        Remove an attribute

        Raises
        ------
        AttributeError
            if the dict is frozen or sealed
        """
        if self._frozen:
            raise AttributeError(
                f"cannot delete attribute '{key}' from frozen easytree.dict"
            )
        if self._sealed:
            raise AttributeError(
                f"cannot delete attribute '{key}' from sealed easytree.dict"
            )
        del self[key]

    def __reduce__(self):
        """
        Pickling
        """
        return self.__class__, (), self.__dict__, None, iter(self.items())

    def __setstate__(self, state):
        """
        Unpickling
        """
        self.__dict__.update(state)

    def setdefault(self, key, default):
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.

        Parameters
        ----------
        key : any
            the key
        default : any
            the default value to insert if the key does not exist

        Raises
        ------
        AttributeError
            if the dict is frozen, or if the dict is sealed and the key does not exist in the dict
        """
        if key not in self:
            if self._frozen:
                raise AttributeError(f"Cannot set {key} on frozen easytree.dict")
            if self._sealed and key not in self:
                raise AttributeError(f"Cannot set {key} on sealed easytree.dict")
            return super().setdefault(
                key, cast(default, sealed=self._sealed, frozen=self._frozen)
            )
        return self[key]

    def get(self, key, default=None):
        """
        Get item by key, if it is exists; otherwise, return default

        If key is list, recursively traverses the tree

        Parameters
        ----------
        key : hashable, list[hashable]
            the key (or path of keys)

        Returns
        -------
        value : any

        Example
        -------
        >>> person = easytree.dict({"age":31, "friends":[{"firstname":"Michael"}]})
        >>> person.get("age")
        31
        >>> person.get("address")
        None
        >>> person.get(["friends",0,"firstname"])
        "Michael"
        >>> person.get(["friends",1,"firstname"])
        None
        >>> person.get(["friends",0,"avatar"],"N/A")
        "N/A"
        """
        if isinstance(key, builtins.list):
            if len(key) == 0:
                return default

            current = self
            while len(key) > 0:
                try:
                    current = current[key.pop(0)]
                except (KeyError, IndexError):
                    return default
                if isinstance(current, undefined):
                    return default
            return current

        return super().get(key, default)

    @classmethod
    def fromkeys(cls, keys, value):
        """
        Create a dict from a set of keys and a fixed value
        """
        return super().fromkeys(keys, cast(value))

    def update(self, other):
        """
        Update the dict from keys and values of another mapping
        object

        Parameters
        ----------
        other : mapping
            other dictionary

        Raises
        ------
        AttributeError
            if the dict is frozen, or if the dict is sealed and a key of other does not exist in the dict
        """
        if self._frozen:
            raise AttributeError(f"Cannot update frozen easytree.dict")
        if self._sealed:
            if any(key not in self for key in other):
                raise AttributeError(
                    f"Cannot update sealed easytree.dict with new keys"
                )
        return super().update(
            {
                k: cast(v, sealed=self._sealed, frozen=self._frozen)
                for k, v in other.items()
            }
        )

    def popitem(self):
        """
        Remove and return the last item (key, value pair)
        inserted into the dictionary

        Raises
        ------
        KeyError
            if the dict is empty

        AttributeError
            if the dict is frozen
            if the dict is sealed
        """
        if self._frozen:
            raise AttributeError(f"Cannot popitem from frozen easytree.dict")
        if self._sealed:
            raise AttributeError(f"Cannot popitem from sealed easytree.dict")
        return super().popitem()

    def pop(self, *args):
        """
        Remove and return an element from a dictionary
        having the given key.

        Parameters
        ----------
        key : any
            the key to pop
        default : any
            the default value, if the key does not exist

        Raises
        ------
        KeyError
            if the given key does not exist, and no default value is given

        AttributeError
            if the dict is frozen, or if the dict is sealed
        """
        if self._frozen:
            raise AttributeError(f"Cannot pop from frozen easytree.dict")
        if self._sealed:
            raise AttributeError(f"Cannot pop from sealed easytree.dict")
        return super().pop(*args)

    def __enter__(self):
        """
        Context manager

        Returns
        -------
        self : dict
            a reference to self
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Context manager
        """
        pass


class undefined:
    """
    Undefined node

    The undefined node can be dynamically cast as a :code:`dict` or :code:`list` node depending on
    mutations called on it (e.g. setting an item, setting at attribute, sorting)

    Parameters
    ----------
    key : hashable
        the key of the undefined value in its parent
    parent : list, dict
        the containing parent

    Example
    -------
    .. code-block::

        >>> import easytree

        >>> person = easytree.dict()
        >>> person.address
        <undefined 'address'>

        >>> person.address.country
        <undefined 'country'>

        >>> person.address.country = "United States"
        >>> person.address.country
        "United States"

        >>> person
        {"address": {"country": "United States"}}
    """

    def __init__(self, parent, key):
        self._key = key
        self._parent = parent

    @property
    def _frozen(self):
        """
        Returns True if parent is frozen (read-only)
        """
        return self._parent._frozen

    @property
    def _sealed(self):
        """
        Returns True if parent is sealed (read-only)
        """
        return self._parent._sealed

    def _cast(self, type):
        """
        Casts to the desired type (dict or list), unless it has already been cast.
        """
        if isinstance(self._parent, undefined):
            self._parent = self._parent._cast(dict)

        if self._key not in self._parent:
            self._parent[self._key] = type(sealed=self._sealed, frozen=self._frozen)

        if not isinstance(self._parent[self._key], type):
            raise TypeError(
                f"undefined node '{self._key}' already cast as a '{'dict' if type is list else 'list'}' node"
            )

        return self._parent[self._key]

    def __enter__(self):
        """
        Return self (read-only)
        """
        if isinstance(self._parent, undefined):
            return self
        if isinstance(self._parent[self._key], undefined):
            return self
        return self._parent[self._key]

    def __exit__(self, *args, **kwargs):
        """
        Context manager
        """
        pass

    def __len__(self):
        """
        Return length of node (read-only)
        """
        if isinstance(self._parent, undefined):
            return 0
        if isinstance(self._parent[self._key], undefined):
            return 0
        return len(self._parent[self._key])

    def __repr__(self):
        """
        Return representation (read-only)
        """
        if isinstance(self._parent, undefined):
            return f"<undefined '{self._key}'>"
        if isinstance(self._parent[self._key], undefined):
            return f"<undefined '{self._key}'>"
        return repr(self._parent[self._key])

    def __bool__(self):
        """
        Return the truthy value of the node (read-only)
        """
        if isinstance(self._parent, undefined):
            return False
        if isinstance(self._parent[self._key], undefined):
            return False
        return bool(self._parent[self._key])

    def __getitem__(self, key):
        """
        Return a new undefined node (read-only)
        """
        if isinstance(self._parent, undefined):
            return undefined(parent=self, key=key)
        if isinstance(self._parent[self._key], undefined):
            return undefined(parent=self, key=key)
        return self._parent[self._key][key]

    def __getattr__(self, key):
        """
        Return a new undefined node (read-only)
        """
        return self[key]

    def __setitem__(self, key, value):
        """
        Cast as dict and set a value at a key

        Returns
        -------
        None
        """
        self._cast(dict)[key] = value

    def __setattr__(self, key, value):
        """
        Set a value at a key, casting the
        undefined value to a dict value

        Returns
        -------
        None
        """
        if key in ["_key", "_parent"]:
            return super().__setattr__(key, value)
        self[key] = value

    def __contains__(self, value):
        """
        Return False (read-only)
        """
        if isinstance(self._parent, undefined):
            return False
        if isinstance(self._parent[self._key], undefined):
            return False
        return value in self._parent[self._key]

    def __iter__(self):
        """
        Iterate over as a list (read-only)
        """
        if isinstance(self._parent, undefined):
            return iter([])
        if isinstance(self._parent[self._key], undefined):
            return iter([])
        return iter(self._parent[self._key])

    def append(self, *args, **kwargs):
        """
        Cast as list and append value
        """
        return self._cast(list).append(*args, **kwargs)

    def extend(self, other):
        """
        Cast as list and extend with other
        """
        return self._cast(list).extend(other)

    def insert(self, index, value):
        """
        Cast as list and insert value at index

        Parameters
        ----------
        index : int
            the index
        value : any
            the value
        """
        return self._cast(list).insert(index, value)

    def remove(self, x):
        """
        Cast as list and remove the first item from the list whose value is equal to x.

        Parameters
        ----------
        x : any
            the value to remove

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        ValueError
            if there is no such item
        """
        return self._cast(list).remove(x)

    def sort(self, *, key=None, reverse=False):
        """
        Cast as list and sort the items in place

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is frozen
        """
        return self._cast(list).sort(key=key, reverse=reverse)

    def reverse(self):
        """
        Cast as list and reverse the elements in place.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            if the list is sealed or frozen
        """
        return self._cast(list).reverse()

    def count(self, value):
        """
        Return number of occurrences of value (read-only).
        """
        if isinstance(self._parent, undefined):
            return 0
        if isinstance(self._parent[self._key], undefined):
            return 0
        return self._parent[self._key].count(value)

    def index(self, value, start=0, stop=9223372036854775807):
        """
        Return first index of value (read-only)
        """
        if isinstance(self._parent, undefined):
            return ValueError(f"{value} is not in the undefined node")
        if isinstance(self._parent[self._key], undefined):
            return ValueError(f"{value} is not in the undefined node")
        return self._parent[self._key].index(value, start, stop)

    def keys(self):
        """
        Return keys of empty the dict (read-only)
        """
        if isinstance(self._parent, undefined):
            return dict().keys()
        if isinstance(self._parent[self._key], undefined):
            return dict().keys()
        return self._parent[self._key].keys()

    def values(self):
        """
        Return values of empty the dict (read-only)
        """
        if isinstance(self._parent, undefined):
            return dict().values()
        if isinstance(self._parent[self._key], undefined):
            return dict().values()
        return self._parent[self._key].values()

    def items(self):
        """
        Return items of empty the dict (read-only)
        """
        if isinstance(self._parent, undefined):
            return dict().items()
        if isinstance(self._parent[self._key], undefined):
            return dict().items()
        return self._parent[self._key].items()

    def get(self, key, default=None):
        """
        Return default value (read-only)

        Parameters
        ----------
        key : hashable
            the key to look-up
        default : any
            the default value if the key does not exist
        """
        if isinstance(self._parent, undefined):
            return default
        if isinstance(self._parent[self._key], undefined):
            return default
        return self._parent.get(key, default=default)

    def setdefault(self, key, default):
        """
        Cast as dict and insert default value at key

        Parameters
        ----------
        key : hashable
            the key to look-up
        default : any
            the default value if the key does not exist
        """
        return self._cast(dict).setdefault(key, default=default)

    def update(self, other):
        """
        Cast as dict and insert items from other

        Parameters
        ----------
        other : mapping
            other dictionary
        """
        return self._cast(dict).update(other)

    def popitem(self):
        """
        Cast as dict and remove and return the last item (key, value pair) inserted into the dictionary

        Raises
        ------
        KeyError
            if the dict is empty

        AttributeError
            if the dict is frozen
            if the dict is sealed
        """
        return self._cast(dict).popitem()

    def pop(self, *args):
        """
        If the node has been cast as a dict:
            remove and return the item under the given key (first argument), otherwse the default

        If the node has been cast as a list:
            remove and return the item at the given position in the list

        Otherwise, raise a KeyError
        """
        if isinstance(self._parent, undefined):
            if len(args) == 2:
                return args[1]
            raise KeyError("Unable to pop from undefined node")

        if isinstance(self._parent[self._key], undefined):
            if len(args) == 2:
                return args[1]
            raise KeyError("Unable to pop from undefined node")

        return self._parent[self._key].pop(args)
