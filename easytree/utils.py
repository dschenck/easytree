import json
import warnings
import builtins

from .tree import Node, serialize


def new(root=None, *, sealed: bool = False, frozen: bool = False):
    """
    Creates a new :code:`easytree.Tree`

    Returns
    -------
    easytree.Tree
    """
    warnings.warn(
        "Creating an easytree.Tree with the easytree.new function will be deprecated in future versions. Use easytree.Tree instead",
        DeprecationWarning,
        stacklevel=2,
    )

    return Node(root, sealed=sealed, frozen=frozen)


def load(stream, *args, frozen=False, sealed=False, **kwargs):
    """
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
    Deserialize s (a str, bytes or bytearray instance containing a JSON document) to an :code:`Tree` object

    :code:`*args` and :code:`**kwargs` are passed to the :code:`json.loads` function
    """
    return Node(json.loads(s, *args, **kwargs), sealed=sealed, frozen=frozen)


def dump(obj, stream, *args, **kwargs):
    """
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
    Serialize :code:`Tree` to a JSON formatted string.

    :code:`*args` and :code:`**kwargs` are passed to the :code:`json.dumps` function
    """
    return json.dumps(serialize(obj), *args, **kwargs)


def frozen(tree):
    """
    Returns :code:`True` if the tree is frozen

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    bool
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return tree._frozen


def freeze(tree):
    """
    Returns a new frozen copy of the tree

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    easytree.Tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, frozen=True)


def unfreeze(tree):
    """
    Returns a new unfrozen copy of the tree

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    easytree.Tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, frozen=False)


def sealed(tree: Node) -> Node:
    """
    Returns :code:`True` if the tree is sealed

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    bool
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return tree._sealed


def seal(tree: Node) -> Node:
    """
    Returns a new sealed copy of the tree

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    easytree.Tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, sealed=False)


def unseal(tree: Node) -> Node:
    """
    Returns a new unsealed copy of the tree

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    unsealed : easytree.Tree
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be instance of easytree.Tree, received {type(tree)}"
        )
    return Node(tree, sealed=False)


def nodetype(tree: Node) -> str:
    """
    Return the node type

    Parameters
    ----------
    tree : easytree.Tree
        an easytree.Tree or Node

    Returns
    -------
    type : str
        one of 'dict', 'list' or 'undefined'
    """
    if not isinstance(tree, Node):
        raise TypeError(
            f"Expected tree to be an instance of easytree.Tree, received {type(tree)}"
        )
    return tree._Node__nodetype
