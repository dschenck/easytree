Changelog
=====================================
The source code is hosted and maintained on `github <https://github.com/dschenck/easytree/>`_.

Version 0.1.0 (2020-08-01)
-------------------------------------
    - created :code:`easytree`

Version 0.1.1 (2020-08-02)
-------------------------------------
    - added ability to :code:`append` dictionary using keyword arguments
    - added ability to iterate over a tree
    - added ability to compute the length of a tree (for list nodes and dict nodes)

Version 0.1.2 (2020-08-03)
-------------------------------------
    - overrode the :code:`__new__` method to filter out primitive and object types
    - added ability to check for contains

Version 0.1.3 (2020-08-04)
-------------------------------------
    - added the :code:`serialize` method to the tree

Version 0.1.4 (2020-08-05)
-------------------------------------
    - added context manager to return a reference to itself
    - addressed infinite recursion in :code:`__getattr__`
    - :code:`append` now returns a reference to last added node, if it is a node

Version 0.1.5 (2020-08-08)
-------------------------------------
    - refactored the :code:`Tree` object into a :code:`Tree` and :code:`Node` object
    - removed the :code:`__new__` from the :code:`Tree` root object to allow for inheritence

Version 0.1.6 (2020-08-16)
-------------------------------------
    - fixed a bug where overriding an attribute would fail if it was already in the node

Version 0.1.7 (2021-05-01)
-------------------------------------
    - passing an :code:`easytree.Tree` object as an instanciation argument will copy the tree
    - added support for list slicing in list nodes
    - improved error messages
    - removed unncessary code in append method
    - factored out constants
    - :code:`repr` now delegates to underlying value
    - addressed ipython canary 
    - added :code:`get` method for dict nodes
    - implemented :code:`__delitem__`, :code:`__delattr__` and :code:`__bool__`

Version 0.1.8 (2021-06-13)
-------------------------------------
    - formatted code using `Black <https://github.com/psf/black>`_ 
    - added convenience i/o functions (e.g. :code:`load` and :code:`dump`)
    - added support for :code:`abc.KeysView` and :code:`abc.ValuesView` values
    - merged root and node classes
    - refactored :code:`__value__` attribute to :code:`_value`
    - added support for freezing and sealing trees

Version 0.1.9 (2021-06-21)
-------------------------------------
    - fixed bug in complex inheritence

Version 0.1.10 (2021-07-03)
-------------------------------------
    - removed AmbiguityError when casting undefined node to dict node with integers