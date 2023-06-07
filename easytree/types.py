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

    Note
    ----
    Values appended to a list node are cast to an :code:`easytree.dict`
    or :code:`easytree.list` types if they are a :code:`dict` or :code:`list`
    """

    def __init__(self, args=None, sealed=False, frozen=False):
        super().__init__(
            [cast(arg, sealed=sealed, frozen=frozen) for arg in (args or [])]
        )
        self._sealed = sealed
        self._frozen = frozen

    def append(self, *args, **kwargs):
        """
        Modified append

        Returns
        -------
        easytree.list
            self
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

        if value is None and len(kwargs) == 0:
            super().append(undefined(self, len(self)))
        elif value is not None:
            super().append(cast(value, sealed=self._sealed, frozen=self._frozen))
        else:
            super().append(cast(kwargs, sealed=self._sealed, frozen=self._frozen))
        return self[len(self) - 1]

    def extend(self, other):
        """
        Returns
        -------
        easytree.list
            self
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot extend frozen or sealed list")
        super().extend(
            [cast(v, sealed=self._sealed, frozen=self._frozen) for v in other]
        )
        return self

    def insert(self, index, value):
        """
        Returns
        -------
        easytree.list
            self
        """
        if self._frozen or self._sealed:
            raise TypeError("cannot insert into frozen or sealed list")
        super().insert(index, cast(value, sealed=self._sealed, frozen=self._frozen))
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass


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

    @classmethod
    def fromkeys(cls, keys, value):
        return super().fromkeys(keys, cast(value))

    def update(self, other):
        return super().update(
            {
                k: cast(v, sealed=self._sealed, frozen=self._frozen)
                for k, v in other.items()
            }
        )

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
            {key: cast(value, self._parent.sealed, frozen=self._parent.frozen)},
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
        return default

    def setdefault(self, key, default):
        self._parent[self.key] = {key: default}
        return self._parent.setdefault(key, default)
