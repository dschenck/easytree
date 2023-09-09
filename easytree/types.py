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
    kwargs : dict
        additional parameters to pass to the easytree.dict or easytree.list
        initialisation (sealed, frozen)

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
        try:
            return self[key]
        except KeyError:
            if self._frozen:
                raise AttributeError(f"Cannot set {key} on frozen easytree.dict")
            if self._sealed and key not in self:
                raise AttributeError(f"Cannot set {key} on sealed easytree.dict")
        return super().setdefault(
            key, cast(default, sealed=self._sealed, frozen=self._frozen)
        )

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
    undefined

    Parameters
    ----------
    key : hashable
        the key of the undefined value in its parent
    parent : list, dict
        the containing parent
    """

    def __init__(self, parent, key):
        self.key = key
        self._parent = parent

    def __bool__(self):
        """
        Return False
        """
        return False

    def __getitem__(self, key):
        """
        Return a new undefined node
        """
        return undefined(parent=self, key=key)

    def __getattr__(self, key):
        """
        Return a new undefined node
        """
        return self[key]

    def __setitem__(self, key, value):
        """
        Set a value at a key, casting the
        undefined value to a dict value

        Returns
        -------
        None
        """
        if self.key in self._parent:
            self._parent[self.key][key] = value
            return

        self._parent[self.key] = dict({key: value})

    def __setattr__(self, key, value):
        """
        Set a value at a key, casting the
        undefined value to a dict value

        Returns
        -------
        None
        """
        if key in ["key", "_parent"]:
            return super().__setattr__(key, value)
        self[key] = value

    def __contains__(self, value):
        """
        Return False
        """
        return False

    def __iter__(self):
        """
        Iterate over empty list
        """
        return iter([])

    def append(self, *args, **kwargs):
        """
        Cast undefined node to list and append value
        """
        if (
            len(args) > 1
            or (len(args) != 0 and len(kwargs) != 0)
            or (len(args) == len(kwargs) == 0)
        ):
            raise ValueError(
                "append must take either one positional argument or one-to-many named arguments"
            )
        value = args[0] if len(args) > 0 else kwargs
        self._parent[self.key] = list([value])
        return self._parent[self.key][-1]

    def extend(self, other):
        """
        Cast undefined node to list and extend with other
        """
        self._parent[self.key] = list(other)

    def get(self, key, default=None):
        """
        Return default value
        """
        return default

    def setdefault(self, key, default):
        """
        Cast node to dict and insert default value at key
        """
        self._parent[self.key] = dict({key: default})

    def update(self, other):
        """
        Cast node to dict and insert items from other
        """
        self._parent[self.key] = dict(other)
        return self._parent

    def __enter__(self):
        """
        Return self
        """
        return self

    def __exit__(self, *args, **kwargs):
        """
        Context manager
        """
        pass

    def __len__(self):
        """
        Return 0
        """
        return 0

    def __repr__(self):
        """
        Return representation
        """
        return f"<Node '{self.key}'>"
