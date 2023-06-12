import builtins


def cast(value=None, *args, **kwargs):
    """
    Converts the value to an easytree type
    """
    if isinstance(value, builtins.dict):
        return dict(value, **kwargs)
    if isinstance(value, (builtins.list, tuple, set, range, zip)):
        return list(value, **kwargs)
    return value


class list(builtins.list):
    """
    List node
    """

    def __init__(self, args=None, sealed=False, frozen=False):
        super().__init__(
            [cast(arg, sealed=sealed, frozen=frozen) for arg in (args or [])]
        )
        self._sealed = sealed
        self._frozen = frozen

    def append(self, *args, **kwargs):
        """
        If provided with a list or a dict, the value is cast to
        an easytree.list or easytree.dict.

        Intentionally returns self
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

        super().append(
            cast(args[0] if args else kwargs, sealed=self._sealed, frozen=self._frozen)
        )
        return self[len(self) - 1]

    def extend(self, other):
        """
        Extend the list by appending all the items from the iterable.
        List or dict items from other are cast to easytree.list or
        easytree.dict values respectively.
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot extend frozen or sealed list")
        super().extend(
            [cast(v, sealed=self._sealed, frozen=self._frozen) for v in other]
        )

    def insert(self, index, value):
        """
        Insert an item at a given position.
        If provided with a list or a dict, the value is cast to
        an easytree.list or easytree.dict
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot insert into frozen or sealed list")
        super().insert(index, cast(value, sealed=self._sealed, frozen=self._frozen))

    def remove(self, x):
        """
        Remove the first item from the list whose value is equal to x.
        It raises a ValueError if there is no such item.
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot remove from frozen or sealed list")
        return super().remove(x)

    def pop(self, *args):
        """
        Remove the item at the given position in the list,
        and return it.
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot pop from frozen or sealed list")
        return super().pop(*args)

    def clear(self):
        """
        Remove all items from the list.
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot clear frozen or sealed list")
        return super().clear()

    def sort(self, *, key=None, reverse=False):
        """
        Sort the items of the list in place
        """
        if self._frozen:
            raise TypeError("cannot sort frozen list")
        return super().sort(key=key, reverse=reverse)

    def reverse(self):
        """
        Reverse the elements of the list in place.
        """
        if self._frozen:
            raise TypeError("cannot reverse frozen list")
        return super().reverse()

    def copy(self):
        """
        Return a shallow copy of the list
        """
        return list(self, frozen=self._frozen, sealed=self._sealed)

    def __enter__(self):
        """
        Context manager returns self
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


class dict(builtins.dict):
    """
    dict node
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

    def __reduce__(self):
        return self.__class__, (), self.__dict__, None, iter(self.items())

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getitem__(self, key):
        """
        Returns a value at a key, or :code:`undefined` if
        key does not exist
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            if self._frozen:
                raise KeyError(f"frozen dict has no value for {key}") from None
            if self._sealed:
                raise KeyError(f"sealed dict has no value for {key}") from None
        return undefined(parent=self, key=key)

    def __setitem__(self, key, value):
        """
        Set a value at a key
        """
        if self._frozen:
            raise KeyError(f"cannot define value for {key} on frozen dict")
        if self._sealed and key not in self:
            raise KeyError(f"sealed define value for {key} on sealed dict")
        super().__setitem__(key, value)

    def __getattr__(self, key):
        """
        Returns a value at a key, or :code:`undefined` if
        key does not exist

        Note
        ----
        if key in :code:`_frozen` or :code:`_sealed`,
        then the instance is an instance of a subclass
        to :code:`easytree.dict` which overrode the
        default :code:`__init__`
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            if key in ["_frozen", "_sealed"]:
                return False  # if subclass overrides the init (see note)
            if self._frozen:
                raise AttributeError(f"frozen dict has not attribute {key}") from None
            if self._sealed:
                raise AttributeError(f"sealed dict has not attribute {key}") from None
        return undefined(parent=self, key=key)

    def __setattr__(self, key, value):
        """
        Sets a value at a key, recursively casting the value
        to a :code:`easytree.dict` or :code:`easytree.list`.
        """
        if key in ["_sealed", "_frozen"]:
            return super().__setattr__(key, value)
        if self._frozen:
            raise AttributeError(f"cannot set attribute {key} on frozen dict")
        if self._sealed and key not in self:
            raise AttributeError(f"cannot define attribute {key} on sealed dict")
        self[key] = cast(value, sealed=self._sealed, frozen=self._frozen)

    def __delattr__(self, key: str) -> None:
        """
        Remove an attribute
        """
        if self._frozen:
            raise AttributeError(f"cannot delete attribute '{key}' on frozen node")
        if self._sealed:
            raise AttributeError(f"cannot delete attribute '{key}' on sealed node")
        del self[key]

    def setdefault(self, key, value):
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        try:
            return self[key]
        except KeyError:
            if self._frozen:
                raise AttributeError(f"Cannot set {key} on frozen node")
            if self._sealed and key not in self:
                raise AttributeError(f"Cannot set {key} on frozen node")
        return super().setdefault(
            key, cast(value, sealed=self._sealed, frozen=self._frozen)
        )

    def get(self, key, default=None):
        """
        Get item by key, it is exists
        Otherwise, return default

        If key is list, traverses the tree
        """
        if isinstance(key, builtins.list):
            if len(key) == 0:
                return cast(default, sealed=self._sealed, frozen=self._frozen)

            current = self
            while len(key) > 0:
                try:
                    current = current[key.pop(0)]
                except (KeyError, IndexError):
                    return cast(default, sealed=self._sealed, frozen=self._frozen)
                if isinstance(current, undefined):
                    return cast(default, sealed=self._sealed, frozen=self._frozen)
            return current

        return super().get(key, cast(default, sealed=self._sealed, frozen=self._frozen))

    @classmethod
    def fromkeys(cls, keys, value):
        return super().fromkeys(keys, cast(value))

    def update(self, other):
        if self._frozen:
            raise AttributeError(f"Cannot update frozen dict")
        if self._sealed:
            if any(key not in self for key in other):
                raise AttributeError(f"Cannot update sealed dict with new keys")
        return super().update(
            {
                k: cast(v, sealed=self._sealed, frozen=self._frozen)
                for k, v in other.items()
            }
        )

    def popitem(self):
        if self._frozen:
            raise AttributeError(f"Cannot popitem from frozen dict")
        if self._sealed:
            raise AttributeError(f"Cannot popitem from sealed dict")
        return super().popitem()

    def pop(self, *args):
        if self._frozen:
            raise AttributeError(f"Cannot pop from frozen dict")
        if self._sealed:
            raise AttributeError(f"Cannot pop from sealed dict")
        return super().pop(*args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


class undefined:
    """
    undefined type
    """

    def __init__(self, parent, key):
        self.key = key
        self._parent = parent

    def __bool__(self):
        return False

    def __getitem__(self, key):
        return undefined(parent=self, key=key)

    def __getattr__(self, key):
        return self[key]

    def __setitem__(self, key, value):
        self._parent[self.key] = dict(
            {key: cast(value, sealed=self._parent.sealed, frozen=self._parent.frozen)},
            sealed=self._parent.sealed,
            frozen=self._parent.frozen,
        )
        return

    def __setattr__(self, key, value):
        if key in ["key", "_parent"]:
            return super().__setattr__(key, value)
        self[key] = value

    def __contains__(self, value):
        return False

    def __iter__(self):
        return iter([])

    def __bool__(self):
        return False

    def append(self, value=None, **kwargs):
        self._parent[self.key] = list([value or kwargs])
        return self._parent[self.key]

    def get(self, key, default=None):
        return cast(default, sealed=self._parent.sealed, frozen=self._parent.frozen)

    def setdefault(self, key, default):
        self._parent[self.key] = {key: default}
        return self._parent.setdefault(key, default)
