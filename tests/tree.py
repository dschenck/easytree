import unittest
import easytree
import easytree.tree

import pickle
import io


class TestTree(unittest.TestCase):
    def test_initialization(self):
        tree = easytree.Tree()
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "undefined")

        tree = easytree.Tree()
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "undefined")

        tree = easytree.Tree({})
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "dict")

        tree = easytree.Tree([])
        self.assertIsInstance(tree, easytree.Tree)
        self.assertEqual(tree._Node__nodetype, "list")

        tree = easytree.tree.Node(1)
        self.assertEqual(tree, 1)
        self.assertIsInstance(tree, int)

        tree = easytree.tree.Node(True)
        self.assertEqual(tree, True)
        self.assertIsInstance(tree, bool)

        foo = easytree.Tree({})
        bar = easytree.Tree(foo)
        self.assertIsNot(foo, bar)

    def test_attribute_lookup(self):
        tree = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert tree.name == "foo"

        with self.assertRaises(AttributeError):
            x = tree.numbers.should_not_exists

    def test_attribute_assignment(self):
        tree = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        with self.assertRaises(AttributeError):
            tree.numbers.name = "XXX"

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

    def test_representation(self):
        tree = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert str(tree) == str(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert repr(tree) == f"Tree({str(tree)})"

    def test_serialization(self):
        tree = easytree.Tree()
        self.assertIsNone(easytree.serialize(tree))

        tree = easytree.Tree({})
        self.assertIsInstance(easytree.serialize(tree), dict)

        tree = easytree.Tree([])
        self.assertIsInstance(easytree.serialize(tree), list)

        tree = easytree.tree.Node(True)
        self.assertIsInstance(easytree.serialize(tree), bool)

        tree = easytree.tree.Node(10)
        self.assertIsInstance(easytree.serialize(tree), int)

        tree = easytree.tree.Node("hello world")
        self.assertIsInstance(easytree.serialize(tree), str)

        tree = easytree.Tree()
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

        tree = easytree.Tree()
        tree.friends = [{"name": "David"}, {"name": "Celine"}]
        tree.friends[0].age = 29
        tree.context.city = "London"
        tree.context.country = "United Kingdom"
        self.assertEqual(set(easytree.serialize(tree)), set(tree.serialize()))

    def test_appending(self):
        tree = easytree.Tree()
        tree.append({"make": "Saab", "color": "blue"})
        tree.append(make="Toyota", color="red")

        self.assertIsInstance(easytree.serialize(tree), list)
        self.assertIsInstance(tree[0], easytree.Tree)
        self.assertIsInstance(tree[1], easytree.Tree)

        tree = easytree.Tree()
        tree.append(None).append(None).append(1)
        self.assertEqual(str(tree.serialize()), "[[[1]]]")

        tree = easytree.Tree({"foo": "bar"})
        self.assertEqual(tree._Node__nodetype, "dict")

        with self.assertRaises(AttributeError):
            tree.append("XXX")

    def test_indexing(self):
        tree = easytree.Tree()

        with self.assertRaises(IndexError):
            tree[0] = "test"

        tree = easytree.Tree([1, 2, 3, 4, 5])
        with self.assertRaises(TypeError):
            tree["A"]

        tree = easytree.Tree()
        tree.append("test")  # convert to list-node
        self.assertEqual(tree[0], "test")

        tree = easytree.Tree({0: "test"})  # convert to dict-node
        self.assertEqual(tree[0], "test")

    def test_slicing(self):
        tree = easytree.Tree([1, 3, 5, 7])
        self.assertEqual(tree[0:2], [1, 3])

    def test_length(self):
        tree = easytree.Tree([1, 2, 3])
        self.assertEqual(len(tree), 3)

        tree = easytree.Tree({"name": "David", "age": 29})
        self.assertEqual(len(tree), 2)

        with self.assertRaises(TypeError):
            len(easytree.Tree(1))

    def test_iteration(self):
        tree = easytree.Tree([1, 2, 3])
        for child in tree:
            self.assertIsInstance(child, int)

        tree = easytree.Tree({"name": "David", "age": 29})
        for child in tree:
            self.assertIsInstance(child, str)

    def test_inheritence(self):
        class Grandchild(easytree.Tree):
            def walk(self):
                return "walking"

        class Child(easytree.Tree):
            def __init__(self, name, age):
                self.child = Grandchild()
                self.name = name
                self.age = age

        instance = Child("Bob", 29)
        instance.address.number = 1
        instance.address.street = "avenue Montaigne"
        instance.address.city = "Paris"
        instance.address.country = "France"

        self.assertIsInstance(instance.address, easytree.Tree)
        self.assertIsInstance(instance.address, easytree.tree.Node)
        self.assertIsInstance(instance.child, Grandchild)
        self.assertEqual(instance.child.walk(), "walking")
        self.assertEqual(
            set(instance.serialize()), set(("child", "name", "age", "address"))
        )
        self.assertEqual(
            set(instance.serialize()["address"]),
            set(("number", "street", "city", "country")),
        )
        self.assertEqual(instance.serialize()["address"]["city"], "Paris")

        # passing subclasses returns instance
        grandchild = Grandchild()
        altinstance = easytree.Tree(grandchild)
        self.assertIsInstance(altinstance, Grandchild)
        self.assertIs(altinstance, grandchild)

        class Child(easytree.Tree):
            def append(self, value, *args, **kwargs):
                super().append(value=value, **kwargs)
                return (value, len(args), len(kwargs))

        instance = Child()

        self.assertIsInstance(instance, easytree.Tree)
        self.assertIsInstance(instance, Child)
        self.assertEqual(instance.append("test"), ("test", 0, 0))
        self.assertEqual(instance.append("test", 1), ("test", 1, 0))
        self.assertEqual(instance.append("test", name="alpha"), ("test", 0, 1))
        self.assertEqual(instance.append("test", True, name="alpha"), ("test", 1, 1))

    def test_contextmanager(self):
        chart = easytree.Tree()

        with chart.axes.append({}) as axis:
            axis.title.text = "primary axis"
        with chart.axes.append({}) as axis:
            axis.title.text = "secondary axis"

        self.assertEqual(chart.axes[0].title.text, "primary axis")
        self.assertEqual(chart.axes[1].title.text, "secondary axis")

    def test_overrides(self):
        tree = easytree.Tree()
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

        assert easytree.frozen(tree) is True
        assert easytree.sealed(tree) is False

        tree = easytree.Tree(tree)

        self.assertFalse(tree.city._frozen, False)

        assert easytree.frozen(tree) is False
        assert easytree.sealed(tree) is False

        with self.assertRaises(TypeError):
            easytree.freeze("Not an easytree")

    def test_frozen_or_sealed_undefined_node(self):
        tree = easytree.Tree(sealed=True)

        with self.assertRaises(AttributeError):
            x = tree.x

        with self.assertRaises(AttributeError):
            tree.x = "should not be assigned"

        tree = easytree.Tree(frozen=True)

        with self.assertRaises(AttributeError):
            x = tree.x

        with self.assertRaises(AttributeError):
            tree.x = "should not be assigned"

    def test_sealing(self):
        tree = easytree.Tree(
            {"name": "David", "address": {"city": "New York"}, "friends": ["Alice"]},
            sealed=True,
        )

        tree.address.city = "Paris"

        with self.assertRaises(Exception):
            tree.address.country = "France"

        assert easytree.frozen(tree) is False
        assert easytree.sealed(tree) is True

        with self.assertRaises(TypeError):
            easytree.seal("Not an easytree")

        tree = easytree.seal(
            easytree.Tree(
                {"name": "David", "address": {"city": "New York"}, "friends": ["Alice"]}
            )
        )

        tree.address.city = "Paris"

        with self.assertRaises(Exception):
            tree.address.country = "France"

        assert easytree.frozen(tree) is False
        assert easytree.sealed(tree) is True

        with self.assertRaises(TypeError):
            easytree.seal("Not an easytree")

    def test_pickling(self):
        this = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        stream = io.BytesIO(pickle.dumps(this))

        that = pickle.load(stream)

        assert isinstance(that, easytree.Tree)
        assert isinstance(that.address, easytree.Tree)
        assert isinstance(that.address.country, str) and that.address.country == "US"

    def test_keys(self):
        tree = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert all([k in tree.keys() for k in ["name", "numbers", "address"]])

        tree = easytree.Tree([1, 2, 3])

        with self.assertRaises(AttributeError):
            keys = tree.keys()

    def test_values(self):
        # dict node
        tree = easytree.Tree(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert list(tree.values()) == ["foo", tree.numbers, tree.address]

        # list node
        tree = easytree.Tree([1, 2, 3])

        with self.assertRaises(AttributeError):
            keys = tree.values()

        # undefined node
        tree = easytree.Tree()
        assert list(tree.values()) == []

    def test_update(self):
        this = easytree.Tree({"a": 1, "b": 2})
        that = easytree.Tree({"b": 3, "c": 4})

        this.update(that)

        assert set(this.keys()) == set(["a", "b", "c"])
        assert this.b == 3
        assert this.c == 4
        assert this.a == 1

        # check the updatand is unchanged
        assert set(that.keys()) == set(["b", "c"])
        assert that.b == 3
        assert that.c == 4

        # check undefined node
        alt = easytree.Tree()
        alt.update(that)

        assert set(that.keys()) == set(["b", "c"])
        assert alt.b == 3
        assert alt.c == 4

        # check deeply nested updates
        tree = easytree.Tree()
        tree.foo.bar.baz = {"a": 1, "b": 2}
        tree.foo.bar.baz.update(that)

        assert tree.serialize() == {"foo": {"bar": {"baz": {"a": 1, "b": 3, "c": 4}}}}

    def test_name_collisions_with_methods(self):
        tree = easytree.Tree({})
        tree.values = 1

        assert tree["values"] == 1
        assert callable(tree.values)  # not to be confused with method...

        setattr(tree, "keys", 2)
        assert tree["keys"] == 2
        assert callable(tree.keys)

    def test_reverse_update(self):
        this = {"age": 29, "country": "US"}
        that = easytree.Tree({"name": "David", "country": "France"})

        this.update(that)

        assert this == {"name": "David", "age": 29, "country": "France"}

    def test_pop(self):
        tree = easytree.Tree(
            {"name": "Bob", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )
        value = tree.pop("name")
        assert value == "Bob"

        assert tree.serialize() == {"numbers": [1, 3, 5], "address": {"country": "US"}}

        value = tree.numbers.pop()
        assert value == 5

        assert tree.serialize() == {"numbers": [1, 3], "address": {"country": "US"}}

    def test_deepget(self):
        tree = easytree.Tree(
            {
                "name": "Bob",
                "children": [{"name": "Alice", "university": {"name": "MIT"}}],
                "address": {"country": "US"},
            }
        )

        assert tree.deepget(("children", 0, "university", "name")) == "MIT"
        assert tree.deepget(("children", 10, "university", "name")) is None
        assert tree.deepget(("address", "city")) is None
        assert tree.deepget(("address", "city"), "New York") == "New York"
