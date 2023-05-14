from easytree.tree import (
    Node,
    serialize,
)

from easytree.utils import (
    new,
    load,
    loads,
    dump,
    dumps,
    frozen,
    freeze,
    unfreeze,
    sealed,
    seal,
    unseal,
    nodetype as type,
)

from easytree.types import dict, list, undefined

# export Node as Tree
Tree = Node
