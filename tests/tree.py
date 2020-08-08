import unittest
import easytree
import easytree.tree

class TestTree(unittest.TestCase):
    def test_initialization(self):
        tree = easytree.new()
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree.__nodetype__, "null")

        tree = easytree.Tree()
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree.__nodetype__, "null")

        tree = easytree.new({})
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree.__nodetype__, "dict")

        tree = easytree.new([])
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree.__nodetype__, "list")

        tree = easytree.tree.Node(1)
        self.assertEqual(tree, 1)
        self.assertIsInstance(tree, int)

        tree = easytree.tree.Node(True)
        self.assertEqual(tree, True)
        self.assertIsInstance(tree, bool)

    def test_serialization(self):
        tree = easytree.new()
        self.assertIsNone(easytree.serialize(tree))

        tree = easytree.new({})
        self.assertIsInstance(easytree.serialize(tree), dict)

        tree = easytree.new([])
        self.assertIsInstance(easytree.serialize(tree), list)

        tree = easytree.tree.Node(True)
        self.assertIsInstance(easytree.serialize(tree), bool)

        tree = easytree.tree.Node(10)
        self.assertIsInstance(easytree.serialize(tree), int)

        tree = easytree.tree.Node("hello world")
        self.assertIsInstance(easytree.serialize(tree), str)

        tree = easytree.new()
        tree.friends = [{"name":"David"}, {"name":"Celine"}]
        tree.friends[0].age = 29
        tree.context.city = "London"
        tree.context.country = "United Kingdom"
        tree = easytree.serialize(tree)

        self.assertIsInstance(tree, dict)
        self.assertIsInstance(tree["friends"], list)
        self.assertIsInstance(tree["context"], dict)
        self.assertEqual(len(tree["context"]), 2)
        self.assertEqual(tree["friends"][0]["age"], 29)

        tree = easytree.new()
        tree.friends = [{"name":"David"}, {"name":"Celine"}]
        tree.friends[0].age = 29
        tree.context.city = "London"
        tree.context.country = "United Kingdom"
        self.assertEqual(set(easytree.serialize(tree)), set(tree.serialize()))

    def test_appending(self):
        tree = easytree.new()
        tree.append({"make":"Saab","color":"blue"})
        tree.append(make="Toyota", color="red")

        self.assertIsInstance(easytree.serialize(tree), list)
        self.assertIsInstance(tree[0], easytree.Tree)
        self.assertIsInstance(tree[1], easytree.Tree)

        tree = easytree.new()
        tree.append(None).append(None).append(1)
        self.assertEqual(str(tree.serialize()), "[[[1]]]")

    def test_indexing(self):
        tree = easytree.new()

        with self.assertRaises(IndexError):
            tree[0] = "test"

        tree = easytree.new()
        tree.append("test") #convert to list-node
        self.assertEqual(easytree.serialize(tree)[0], "test")

        tree = easytree.new({0:"test"}) #convert to dict-node
        self.assertEqual(easytree.serialize(tree)[0], "test")

    def test_length(self):
        tree = easytree.new([1,2,3])
        self.assertEqual(len(tree), 3)

        tree = easytree.new({"name":"David","age":29})
        self.assertEqual(len(tree), 2)

        with self.assertRaises(TypeError):
            len(easytree.new(1))

    def test_iteration(self):
        tree = easytree.new([1,2,3])
        for child in tree: 
            self.assertIsInstance(child, int)

        tree = easytree.new({"name":"David","age":29})
        for child in tree: 
            self.assertIsInstance(child, str)

    def test_inheritence(self):
        
        class Child(easytree.Tree):
            def __init__(self, name, age):
                self.name = name
                self.age  = age

        instance = Child("Bob", 29)
        instance.address.number = 1
        instance.address.street = "avenue Montaigne"
        instance.address.city = "Paris"
        instance.address.country = "France"
        
        self.assertEqual(set(instance.serialize()), set(("name","age","address")))
        self.assertEqual(set(instance.serialize()["address"]), set(("number","street","city","country")))
        self.assertEqual(instance.serialize()["address"]["city"], "Paris")

    def test_contextmanager(self):
        chart = easytree.new()

        with chart.axes.append({}) as axis: 
            axis.title.text = "primary axis"
        with chart.axes.append({}) as axis: 
            axis.title.text = "secondary axis"

        self.assertEqual(chart.axes[0].title.text, "primary axis")
        self.assertEqual(chart.axes[1].title.text, "secondary axis")

