import unittest
import easytree
import easytree.types

import pickle
import io


class TestTree(unittest.TestCase):
    def test_initialization(self):
        tree = easytree.types.Node(1)
        self.assertEqual(tree, 1)
        self.assertIsInstance(tree, int)

        tree = easytree.types.Node(True)
        self.assertEqual(tree, True)
        self.assertIsInstance(tree, bool)

        foo = easytree.types.dict({})
        bar = easytree.types.dict(foo)
        self.assertIsNot(foo, bar)

    def test_attribute_lookup(self):
        tree = easytree.dict(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert tree.name == "foo"

        with self.assertRaises(AttributeError):
            x = tree.numbers.should_not_exists

    def test_attribute_assignment(self):
        tree = easytree.dict(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert isinstance(tree.numbers, easytree.list)

        tree.numbers.name = "XXX"

        assert isinstance(tree.numbers, easytree.list)
        assert tree.numbers == [1, 3, 5]
        assert tree.numbers != [1, 4, 5]

    def test_fromkeys(self):
        tree = easytree.dict.fromkeys([1, 2, 3], {"hello": "world"})
        assert isinstance(tree, easytree.dict)
        assert isinstance(tree[1], easytree.dict)
        assert len(tree) == 3

    def test_copy(self):
        this = easytree.dict(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )
        that = easytree.dict(this)

        self.assertIsInstance(that, easytree.dict)

        that.name = "bar"
        self.assertEqual(this.name, "foo")
        self.assertEqual(that.name, "bar")

        this.numbers.append(7)
        self.assertEqual(that.numbers, [1, 3, 5])
        self.assertEqual(this.numbers, [1, 3, 5, 7])

        this.address.country = "France"
        self.assertEqual(this.address.country, "France")
        self.assertEqual(that.address.country, "US")

    def test_representation(self):
        tree = easytree.dict(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert str(tree) == str(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert repr(tree) == repr(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

    def test_serialization(self):
        tree = easytree.dict({})
        self.assertIsInstance(tree, dict)

        tree = easytree.list()
        self.assertIsInstance(tree, list)

        tree = easytree.types.Node(True)
        self.assertIsInstance(tree, bool)

        tree = easytree.types.Node(10)
        self.assertIsInstance(tree, int)

        tree = easytree.types.Node("hello world")
        self.assertIsInstance(easytree.serialize(tree), str)

        tree = easytree.dict()
        tree.friends = [{"name": "David"}, {"name": "Celine"}]
        tree.friends[0].age = 29
        tree.context.city = "London"
        tree.context.country = "United Kingdom"

        self.assertIsInstance(tree, dict)
        self.assertIsInstance(tree["friends"], list)
        self.assertIsInstance(tree["context"], dict)
        self.assertEqual(len(tree["context"]), 2)
        self.assertEqual(tree["friends"][0]["age"], 29)

    def test_appending(self):
        tree = easytree.list()
        tree.append({"make": "Saab", "color": "blue"})
        tree.append(make="Toyota", color="red")

        self.assertIsInstance(tree, list)
        self.assertIsInstance(tree[0], easytree.dict)
        self.assertIsInstance(tree[1], easytree.dict)

        tree = easytree.dict({"foo": "bar"})
        self.assertIsInstance(tree, dict)

    def test_indexing(self):
        tree = easytree.list()

        with self.assertRaises(IndexError):
            tree[0] = "test"

        tree = easytree.list([1, 2, 3, 4, 5])
        with self.assertRaises(TypeError):
            tree["A"]

        tree = easytree.list()
        tree.append("test")  # convert to list-node
        self.assertEqual(tree[0], "test")

        tree = easytree.dict({0: "test"})  # convert to dict-node
        self.assertEqual(tree[0], "test")

    def test_slicing(self):
        tree = easytree.list([1, 3, 5, 7])
        self.assertEqual(tree[0:2], [1, 3])

    def test_length(self):
        tree = easytree.list([1, 2, 3])
        self.assertEqual(len(tree), 3)

        tree = easytree.dict({"name": "David", "age": 29})
        self.assertEqual(len(tree), 2)

    def test_iteration(self):
        tree = easytree.list([1, 2, 3])
        for child in tree:
            self.assertIsInstance(child, int)

        tree = easytree.dict({"name": "David", "age": 29})
        for child in tree:
            self.assertIsInstance(child, str)

    def test_inheritence(self):
        class Grandchild(easytree.dict):
            def walk(self):
                return "walking"

        class Child(easytree.dict):
            def __init__(self, name, age):
                self.adult = age >= 18
                super().__init__({"name": name, "age": age, "child": Grandchild()})

            def own_method(self):
                return True

        instance = Child("Bob", 29)
        instance.address.number = 1
        instance.address.street = "avenue Montaigne"
        instance.address.city = "Paris"
        instance.address.country = "France"

        self.assertIsInstance(instance, Child)
        self.assertIsInstance(instance.address, easytree.dict)
        self.assertIsInstance(instance.child, easytree.dict)

        assert instance.adult == True
        assert instance.own_method() == True

        class Child(easytree.list):
            def append(self, value, *args, **kwargs):
                super().append(value=value, **kwargs)
                return (value, len(args), len(kwargs))

        instance = Child()

        self.assertIsInstance(instance, easytree.list)
        self.assertIsInstance(instance, Child)
        self.assertEqual(instance.append("test"), ("test", 0, 0))
        self.assertEqual(instance.append("test", 1), ("test", 1, 0))
        self.assertEqual(instance.append("test", name="alpha"), ("test", 0, 1))
        self.assertEqual(instance.append("test", True, name="alpha"), ("test", 1, 1))

    def test_overrides(self):
        tree = easytree.dict()
        tree.title.text = 1

        self.assertEqual(str(tree), str({"title": {"text": 1}}))

        tree.title = None
        self.assertEqual(str(tree), str({"title": None}))

    def test_get(self):
        tree = easytree.dict()
        self.assertEqual(tree.get("foo"), None)
        self.assertEqual(tree.get("foo", "bar"), "bar")

        tree = easytree.dict({"foo": "bar"})
        self.assertEqual(tree.get("foo"), "bar")
        self.assertEqual(tree.get("baz"), None)
        self.assertEqual(tree.get("baz", 29), 29)

        tree = easytree.list([1, 3, 5, 6, 7])
        with self.assertRaises(AttributeError):
            tree.get("foo")

    def test_mutability(self):
        tree = easytree.dict({"foo": "bar", "baz": [1, 3, 5, 7, 9]})
        del tree["foo"]
        self.assertFalse("foo" in tree)

        tree = easytree.dict({"foo": {"bar": "baz"}})
        del tree.foo.bar
        self.assertTrue("foo" in tree)
        self.assertFalse("baz" in tree.foo)

    def test_truthfulness(self):
        tree = easytree.dict()

        if tree:
            raise Exception("An undefined node should be falsy")
        if tree.abc:
            raise Exception("An undefined node should be falsy")

    def test_keys(self):
        tree = easytree.dict(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert all([k in tree.keys() for k in ["name", "numbers", "address"]])

        tree = easytree.list([1, 2, 3])

        with self.assertRaises(AttributeError):
            keys = tree.keys()

    def test_values(self):
        # dict node
        tree = easytree.dict(
            {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )

        assert isinstance(tree.numbers, list)
        assert list(tree.values()) == ["foo", tree.numbers, tree.address]

        # list node
        tree = easytree.list([1, 2, 3])

        with self.assertRaises(AttributeError):
            keys = tree.values()

        # undefined node
        # tree = easytree.Tree()
        # assert list(tree.values()) == []

    def test_update(self):
        this = easytree.dict({"a": 1, "b": 2})
        that = easytree.dict({"b": 3, "c": 4})

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
        alt = easytree.dict()
        alt.update(that)

        assert set(that.keys()) == set(["b", "c"])
        assert alt.b == 3
        assert alt.c == 4

        # check deeply nested updates
        tree = easytree.dict()
        tree.foo.bar.baz = {"a": 1, "b": 2}
        tree.foo.bar.baz.update(that)

        assert tree == {"foo": {"bar": {"baz": {"a": 1, "b": 3, "c": 4}}}}

    def test_name_collisions_with_methods(self):
        tree = easytree.dict({})
        tree.values = 1

        assert tree["values"] == 1
        assert callable(tree.values)  # not to be confused with method...

        setattr(tree, "keys", 2)
        assert tree["keys"] == 2
        assert callable(tree.keys)

    def test_reverse_update(self):
        this = {"age": 29, "country": "US"}
        that = easytree.dict({"name": "David", "country": "France"})

        this.update(that)

        assert this == {"name": "David", "age": 29, "country": "France"}

    def test_pop(self):
        tree = easytree.dict(
            {"name": "Bob", "numbers": [1, 3, 5], "address": {"country": "US"}}
        )
        value = tree.pop("name")
        assert value == "Bob"

        assert tree == {"numbers": [1, 3, 5], "address": {"country": "US"}}

        value = tree.numbers.pop()
        assert value == 5

        assert tree == {"numbers": [1, 3], "address": {"country": "US"}}
