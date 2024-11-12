import builtins

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
    if not isinstance(tree, (dict, list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
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
    if not isinstance(tree, (dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
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
    if not isinstance(tree, (dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
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
    if not isinstance(tree, (dict, list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
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
    if not isinstance(tree, (dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
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
    if not isinstance(tree, (dict, list, builtins.dict, builtins.list)):
        raise TypeError(
            f"Expected tree to be instance of :code:`easytree.dict` or :code:`easytree.list`, received {type(tree)}"
        )
    return cast(tree, sealed=False)
