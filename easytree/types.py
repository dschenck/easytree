import builtins


class Node:
    def __new__(cls, value=None, *args, **kwargs):
        if cls is not Node:
            return super().__new__(cls)
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
            [Node(arg, sealed=sealed, frozen=frozen) for arg in (args or [])]
        )
        self._sealed = sealed
        self._frozen = frozen

    def append(self, value=None, **kwargs):
        """
        Modified append

        Returns
        -------
        easytree.list
            self
        """
        if value is None and len(kwargs) == 0:
            super().append(undefined(self, len(self)))
        elif value is not None:
            super().append(Node(value, sealed=self._sealed, frozen=self._frozen))
        else:
            super().append(Node(kwargs, sealed=self._sealed, frozen=self._frozen))
        return self[len(self) - 1]

    def extend(self, other):
        """
        Returns
        -------
        easytree.list
            self
        """
        super().extend(
            [Node(v, sealed=self._sealed, frozen=self._frozen) for v in other]
        )
        return self

    def insert(self, index, value):
        """
        Returns
        -------
        easytree.list
            self
        """
        super().insert(
            index, Node(value=value, sealed=self._sealed, frozen=self._frozen)
        )
        return self


class dict(builtins.dict):
    """
    dict node
    """

    def __init__(self, *args, sealed=False, frozen=False, **kwargs):
        super().__init__(
            {
                k: Node(v, sealed=sealed, frozen=frozen)
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
        if key in self:
            return super().__getitem__(key)
        return undefined(parent=self, key=key)

    def __getattr__(self, key):
        """
        Returns a value at a key, or :code:`undefined` if
        key does not exist
        """
        return self[key]

    def __setattr__(self, key, value):
        """
        Sets a value at a key, recursively casting the value
        to a :code:`easytree.dict` or :code:`easytree.list`.
        """
        if key in ["_sealed", "_frozen"]:
            return super().__setattr__(key, value)
        self[key] = Node(value, sealed=self._sealed, frozen=self._frozen)
        return

    def __delattr__(self, key: str) -> None:
        """
        Remove an attribute
        """
        del self[key]

    def setdefault(self, key, value):
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        return super().setdefault(
            key, Node(value, sealed=self._sealed, frozen=self._frozen)
        )

    @classmethod
    def fromkeys(cls, keys, value):
        return super().fromkeys(keys, Node(value))

    def update(self, other):
        return super().update(
            {
                k: Node(v, sealed=self._sealed, frozen=self._frozen)
                for k, v in other.items()
            }
        )


class undefined:
    """
    undefined node
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
            {key: Node(value, self._parent.sealed, frozen=self._parent.frozen)},
            sealed=self._parent.sealed,
            frozen=self._parent.frozen,
        )
        return

    def __setattr__(self, key, value):
        if key in ["key", "_parent"]:
            return super().__setattr__(key, value)
        self[key] = value
        return

    def append(self, arg, **kwargs):
        self._parent[self.key] = list([])
        self._parent[self.key].append(arg, **kwargs)
        return self._parent[self.key]

    def get(self, key, default=None):
        return default

    def setdefault(self, key, default):
        self._parent[self.key] = {key: default}
        return self._parent.setdefault(key, default)
