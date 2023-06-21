import json
import warnings
import builtins

from .tree import Node, serialize
from .types import dict, list, cast


def frozen(tree):
    """
    Returns :code:`True` if the tree is frozen

    Parameters
    ----------
    tree
        list or dict

    Returns
    -------
    bool
    """
    if not isinstance(tree, (Node, dict, list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.Tree`, :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    return tree._frozen


def freeze(tree):
    """
    Returns a new frozen copy of the tree

    Parameters
    ----------
    tree
        list or dict

    Returns
    -------
    frozen : dict | list
    """
    if not isinstance(tree, (Node, dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.Tree`, :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    if isinstance(tree, Node):
        return Node(tree, frozen=True)
    return cast(tree, frozen=True)


def unfreeze(tree):
    """
    Returns a new unfrozen copy of the tree

    Parameters
    ----------
    tree
        list or dict

    Returns
    -------
    unfrozen : dict | list
    """
    if not isinstance(tree, (Node, dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.Tree`, :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    if isinstance(tree, Node):
        return Node(tree, frozen=False)
    return cast(tree, frozen=False)


def sealed(tree):
    """
    Returns :code:`True` if the tree is sealed

    Parameters
    ----------
    tree
        list or dict

    Returns
    -------
    bool
    """
    if not isinstance(tree, (Node, dict, list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.Tree`, :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    return tree._sealed


def seal(tree):
    """
    Returns a new sealed copy of the tree

    Parameters
    ----------
    tree
        list or dict

    Returns
    -------
    sealed : dict | list
    """
    if not isinstance(tree, (Node, dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.Tree`, :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    if isinstance(tree, Node):
        return Node(tree, sealed=True)
    return cast(tree, sealed=True)


def unseal(tree):
    """
    Returns a new unsealed copy of the tree

    Parameters
    ----------
    tree
        list or dict

    Returns
    -------
    unsealed : dict | list
    """
    if not isinstance(tree, (Node, dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.Tree`, :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    if isinstance(tree, Node):
        return Node(tree, sealed=False)
    return cast(tree, sealed=False)


def new(root=None, *, sealed: bool = False, frozen: bool = False):
    """
    .. attention:: Deprecated since 0.2.0

    Creates a new :code:`easytree.Tree`

    Returns
    -------
    easytree.Tree


    """
    warnings.warn(
        "easytree.new will be deprecated in future versions. Use :code:`easytree.dict` or :code:`easytree.list` instead",
        DeprecationWarning,
        stacklevel=2,
    )

    return Node(root, sealed=sealed, frozen=frozen)


def load(stream, *args, frozen=False, sealed=False, **kwargs):
    """
    .. attention:: Deprecated since 0.2.0

    Deserialize a text file or binary file containing a JSON document to an :code:`Tree` object


    :code:`*args` and :code:`**kwargs` are passed to the :code:`json.load` function

    Example
    -------------
    >>> with open("data.json", "r") as file:
    ...     tree = easytree.load(file)
    """
    return Node(json.load(stream, *args, **kwargs), sealed=sealed, frozen=frozen)


def loads(s, *args, frozen=False, sealed=False, **kwargs):
    """
    .. attention:: Deprecated since 0.2.0

    Deserialize s (a str, bytes or bytearray instance containing a JSON document) to an :code:`Tree` object

    :code:`*args` and :code:`**kwargs` are passed to the :code:`json.loads` function
    """
    return Node(json.loads(s, *args, **kwargs), sealed=sealed, frozen=frozen)


def dump(obj, stream, *args, **kwargs):
    """
    .. attention:: Deprecated since 0.2.0

    Serialize :code:`Tree` object as a JSON formatted string to stream (a .write()-supporting file-like object).

    :code:`*args` and :code:`**kwargs` are passed to the :code:`json.dump` function

    Example
    -------------
    >>> tree = easytree.Tree({"foo": "bar"})
    >>> with open("data.json", "w") as file:
    ...     easytree.dump(tree, file, indent=4)
    """
    return json.dump(serialize(obj), stream, *args, **kwargs)


def dumps(obj, *args, **kwargs):
    """
    .. attention:: Deprecated since 0.2.0

    Serialize :code:`Tree` to a JSON formatted string.

    :code:`*args` and :code:`**kwargs` are passed to the :code:`json.dumps` function
    """
    return json.dumps(serialize(obj), *args, **kwargs)
