import unittest
import easytree

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

    def test_serialization(self):
        tree = easytree.new()
        self.assertIsNone(easytree.serialize(tree))

        tree = easytree.new({})
        self.assertIsInstance(easytree.serialize(tree), dict)

        tree = easytree.new([])
        self.assertIsInstance(easytree.serialize(tree), list)

        tree = easytree.new(True)
        self.assertIsInstance(easytree.serialize(tree), bool)

        tree = easytree.new(10)
        self.assertIsInstance(easytree.serialize(tree), int)

        tree = easytree.new("hello world")
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

    def test_appending(self):
        tree = easytree.new()
        tree.append({"make":"Saab","color":"blue"})

        self.assertIsInstance(easytree.serialize(tree), list)
        self.assertIsInstance(tree[0], easytree.Tree)