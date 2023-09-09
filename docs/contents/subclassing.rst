Subclassing
-----------
Starting with version 0.2.1., subclassing :code:`easytree.dict` and :code:`easytree.list` classes is possible. 

.. attention:: 
    The only requirement is to keep the signature of the :code:`__init__` method unchanged in your subclass. You may amend the actual method, but the signature should remain the same.

.. code-block:: python

    >>> import easytree 

    >>> class Person(easytree.dict):
    ...     def __init__(self, *args, sealed=False, frozen=False, **kwargs):
    ...         super().__init__(*args, sealed=sealed, frozen=frozen, **kwargs)
    ...
    ...     def greet(self):
    ...         return f"Hello, my name is {self.firstname}"

    >>> class Group(easytree.list): 
    ...     def def __init__(self, args=None, *, sealed=False, frozen=False):
    ...         super().__init__(args, sealed=sealed, frozen=frozen)
    ...
    ...     @property 
    ...     def eldest(self):
    ...         return sorted(self, key=lambda person: person.age)[-1]


    >>> group = Group(
    ...    [
    ...        Person(firstname="Sally",lastname="S", age=35),
    ...        Person(firstname="Alice",lastname="G", age=32)
    ...    ], 
    ...    frozen=True
    ... )

    >>> group.eldest.greet()
    'Hello, my name is Sally'

    >>> easytree.frozen(group[0]) 
    True


    