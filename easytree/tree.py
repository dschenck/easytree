class Tree:
    __hash__ = None 
    
    def __init__(self, value=None):
        if isinstance(value, dict):
            value = {k:Tree(v) for k,v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            value = [Tree(v) for v in value]
        elif isinstance(value, Tree):
            value = value.__value__
        self.__value__ = value
        
    def __repr__(self):
        return f"<Tree type={self.__nodetype__}>"
    
    def __str__(self):
        return str(serialize(self))
        
    @property
    def __nodetype__(self): 
        if self.__value__ is None: 
            return "null"
        if isinstance(self.__value__, list):
            return "list"
        if isinstance(self.__value__, dict):
            return "dict"
        return "object"
    
    def __getattr__(self, name):
        if self.__nodetype__ in ["null", "dict"]:
            if self.__nodetype__ == "null":
                self.__value__ = {}
            if name not in self.__value__: 
                self.__value__[name] = Tree()
            return self.__value__[name]
        return self.__value__.__getattr__(name)
    
    def __setattr__(self, name, value):
        if name == "__value__":
            return super().__setattr__(name, value)
        if self.__nodetype__ == "null":
            self.__value__ = {}
        if self.__nodetype__ == "dict": 
            if name not in self.__value__: 
                self.__value__[name] = Tree(value)
            self.__value__[name]
            return
        return self.__value__.__setattr__(name, value)
        
    def __getitem__(self, name):
        if self.__nodetype__ == "null":
            if isinstance(name, int): 
                raise IndexError("list index out of range")
            else:
                self.__value__ = {}
        if self.__nodetype__ == "dict": 
            if name not in self.__value__: 
                self.__value__[name] = Tree()
            return self.__value__[name]
        if self.__nodetype__ == "list": 
            if not isinstance(name, int): 
                raise IndexError(f"Cannot index list with {type(name)}")
            return self.__value__[name]
        return self.__value__.__getitem__(name)
        
    def __setitem__(self, name, value):
        if self.__nodetype__ == "null":
            if isinstance(name, int):
                raise IndexError("list assignment index out of range")
            self.__value__ = {}
        if self.__nodetype__ == "dict": 
            if name not in self.__value__: 
                self.__value__[name] = Tree(value)
            return
        if self.__nodetype__ == "list": 
            if not isinstance(name, int): 
                raise IndexError(f"Cannot index list with {type(name)}")
            self.__value__[name] = Tree(value)
            return
        return self.__value__.__setitem__(name, value)
        
    def append(self, value):
        """
        Appends a value to a list node (tree branch). If the node type was previously undefined, the node becomes a list. Otherwise, it delegates the call to the underlying value object. 

        Raises
        ---------
        ValueError
            if the node is not a list node

        Example
        ---------
        >>> tree = easytree.new() #undefined node
        >>> tree.append("hello world") #casts node to list
        >>> easytree.serialize(tree)
        ["Hello world"]

        """
        if self.__nodetype__ == "null":
            self.__value__ = []        
        if self.__nodetype__ == "list":
            if isinstance(value, (list, tuple, set)):
                value = [Tree(v) for v in value]
            elif isinstance(value, dict):
                value = Tree({k:Tree(v) for k,v in value.items()})
            else:
                value = Tree(value)
            return self.__value__.append(value)
        raise ValueError("Tree is not a list")
    
def serialize(tree):
    """
    Converts an :code:`easytree.Tree` to a native python type.
    """
    if tree.__nodetype__ == "null":
        return None
    if tree.__nodetype__ == "list":
        return [serialize(value) for value in tree.__value__]
    if tree.__nodetype__ == "dict":
        return {key:serialize(value) for key, value in tree.__value__.items()}
    return tree.__value__


def new(root=None): 
    """
    Creates an :code:`easytree.Tree`
    """
    return Tree(root)