import unittest
import easytree
import easytree.tree


class TestTree(unittest.TestCase):
    def test_initialization(self):
        tree = easytree.new()
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "undefined")

        tree = easytree.Tree()
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "undefined")

        tree = easytree.new({})
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "dict")

        tree = easytree.new([])
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "list")

        tree = easytree.tree.Node(1)
        self.assertEqual(tree, 1)
        self.assertIsInstance(tree, int)

        tree = easytree.tree.Node(True)
        self.assertEqual(tree, True)
        self.assertIsInstance(tree, bool)

    def test_copy(self):
        this = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )
        that = easytree.Tree(this)

        self.assertIsInstance(that, easytree.Tree)
        self.assertEqual(that._Node__nodetype, "dict")

        that.name = "bar"
        self.assertEqual(this.name, "foo")
        self.assertEqual(that.name, "bar")

        this.numbers.append(7)
        self.assertEqual(that.numbers._value, [1, 3, 5])
        self.assertEqual(this.numbers._value, [1, 3, 5, 7])

        this.address.country = "France"
        self.assertEqual(this.address.country, "France")
        self.assertEqual(that.address.country, "US")

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
        tree.friends = [{"name": "David"}, {"name": "Celine"}]
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
        tree.friends = [{"name": "David"}, {"name": "Celine"}]
        tree.friends[0].age = 29
        tree.context.city = "London"
        tree.context.country = "United Kingdom"
        self.assertEqual(set(easytree.serialize(tree)), set(tree.serialize()))

    def test_appending(self):
        tree = easytree.new()
        tree.append({"make": "Saab", "color": "blue"})
        tree.append(make="Toyota", color="red")

        self.assertIsInstance(easytree.serialize(tree), list)
        self.assertIsInstance(tree[0], easytree.Tree)
        self.assertIsInstance(tree[1], easytree.Tree)

        tree = easytree.new()
        tree.append(None).append(None).append(1)
        self.assertEqual(str(tree.serialize()), "[[[1]]]")

        tree = easytree.new({"foo": "bar"})
        self.assertEqual(tree._Node__nodetype, "dict")

        with self.assertRaises(AttributeError):
            tree.append("XXX")

    def test_indexing(self):
        tree = easytree.new()

        with self.assertRaises(IndexError):
            tree[0] = "test"

        tree = easytree.new([1, 2, 3, 4, 5])
        with self.assertRaises(TypeError):
            tree["A"]

        tree = easytree.new()
        tree.append("test")  # convert to list-node
        self.assertEqual(tree[0], "test")

        tree = easytree.new({0: "test"})  # convert to dict-node
        self.assertEqual(tree[0], "test")

    def test_slicing(self):
        tree = easytree.new([1, 3, 5, 7])
        self.assertEqual(tree[0:2], [1, 3])

    def test_length(self):
        tree = easytree.new([1, 2, 3])
        self.assertEqual(len(tree), 3)

        tree = easytree.new({"name": "David", "age": 29})
        self.assertEqual(len(tree), 2)

        with self.assertRaises(TypeError):
            len(easytree.new(1))

    def test_iteration(self):
        tree = easytree.new([1, 2, 3])
        for child in tree:
            self.assertIsInstance(child, int)

        tree = easytree.new({"name": "David", "age": 29})
        for child in tree:
            self.assertIsInstance(child, str)

    def test_inheritence(self):
        class Child(easytree.Tree):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        instance = Child("Bob", 29)
        instance.address.number = 1
        instance.address.street = "avenue Montaigne"
        instance.address.city = "Paris"
        instance.address.country = "France"

        self.assertIsInstance(instance.address, easytree.Tree)
        self.assertIsInstance(instance.address, easytree.tree.Node)
        self.assertEqual(set(instance.serialize()), set(("name", "age", "address")))
        self.assertEqual(
            set(instance.serialize()["address"]),
            set(("number", "street", "city", "country")),
        )
        self.assertEqual(instance.serialize()["address"]["city"], "Paris")

    def test_contextmanager(self):
        chart = easytree.new()

        with chart.axes.append({}) as axis:
            axis.title.text = "primary axis"
        with chart.axes.append({}) as axis:
            axis.title.text = "secondary axis"

        self.assertEqual(chart.axes[0].title.text, "primary axis")
        self.assertEqual(chart.axes[1].title.text, "secondary axis")

    def test_overrides(self):
        tree = easytree.new()
        tree.title.text = 1

        self.assertEqual(str(tree.serialize()), str({"title": {"text": 1}}))

        tree.title = None
        self.assertEqual(str(tree.serialize()), str({"title": None}))

    def test_get(self):
        tree = easytree.Tree()
        self.assertEqual(tree.get("foo"), None)
        self.assertEqual(tree.get("foo", "bar"), "bar")

        tree = easytree.Tree({"foo": "bar"})
        self.assertEqual(tree.get("foo"), "bar")
        self.assertEqual(tree.get("baz"), None)
        self.assertEqual(tree.get("baz", 29), 29)

        tree = easytree.Tree([1, 3, 5, 6, 7])
        with self.assertRaises(AttributeError):
            tree.get("foo")

    def test_mutability(self):
        tree = easytree.Tree({"foo": "bar", "baz": [1, 3, 5, 7, 9]})
        del tree["foo"]
        self.assertFalse("foo" in tree)

        tree = easytree.Tree({"foo": {"bar": "baz"}})
        del tree.foo.bar
        self.assertTrue("foo" in tree)
        self.assertFalse("baz" in tree.foo)

    def test_truthfulness(self):
        tree = easytree.Tree()

        if tree:
            raise Exception("An undefined node should be falsy")
        if tree.abc:
            raise Exception("An undefined node should be falsy")

    def test_sealed(self):
        tree = easytree.Tree(
            {"name": "David", "address": {"city": "New York"}, "friends": ["Alice"]},
            sealed=True,
        )

        self.assertEqual(tree.name, "David")
        self.assertEqual(tree.address.city, "New York")

        tree.name = "Celine"
        tree.address.city = "Los Angeles"

        self.assertEqual(tree.name, "Celine")
        self.assertEqual(tree.address.city, "Los Angeles")

        with self.assertRaises(AttributeError):
            tree.age

        with self.assertRaises(AttributeError):
            tree.address.country

        with self.assertRaises(AttributeError):
            tree.age = 29

        with self.assertRaises(AttributeError):
            tree.address.country = "US"

        self.assertEqual(tree["name"], "Celine")

        with self.assertRaises(KeyError):
            tree["age"]

        with self.assertRaises(TypeError):
            tree["age"] = 29

        with self.assertRaises(TypeError):
            del tree["name"]

        # you can still edit values
        tree.friends[0] = "Thomas"

        # you can't add new items
        with self.assertRaises(TypeError):
            tree.friends.append(name="Charlie")

        tree = easytree.Tree(tree)

        self.assertFalse(tree.city._sealed, False)

    def test_frozen(self):
        tree = easytree.Tree(
            {"name": "David", "address": {"city": "New York"}, "friends": ["Alice"]},
            frozen=True,
        )

        self.assertEqual(tree.name, "David")
        self.assertEqual(tree.address.city, "New York")

        with self.assertRaises(AttributeError):
            tree.name = "Celine"

        with self.assertRaises(AttributeError):
            tree.address.city = "Los Angeles"

        with self.assertRaises(AttributeError):
            tree.age

        with self.assertRaises(AttributeError):
            tree.address.country

        with self.assertRaises(AttributeError):
            tree.age = 29

        with self.assertRaises(AttributeError):
            tree.address.country = "US"

        self.assertEqual(tree["name"], "David")

        with self.assertRaises(KeyError):
            tree["age"]

        with self.assertRaises(TypeError):
            tree["age"] = 29

        with self.assertRaises(TypeError):
            del tree["name"]

        with self.assertRaises(TypeError):
            tree.friends[0] = "Thomas"

        with self.assertRaises(TypeError):
            tree.friends.append("Charlie")

        tree = easytree.Tree(tree)

        self.assertFalse(tree.city._frozen, False)
