import easytree
import easytree.types
import pytest
import pickle
import io
import json


def test_isinstance():
    tree = easytree.dict()
    assert isinstance(tree, dict)

    tree = easytree.list()
    assert isinstance(tree, list)


def test_recursive_behavior():
    tree = easytree.dict({})
    assert isinstance(tree, dict)

    tree = easytree.list()
    assert isinstance(tree, list)

    tree = easytree.dict()
    tree.friends = [{"name": "David"}, {"name": "Celine"}]
    tree.friends[0].age = 29
    tree.context.city = "London"
    tree.context.country = "United Kingdom"

    assert isinstance(tree, easytree.dict)
    assert isinstance(tree["friends"], easytree.list)
    assert isinstance(tree.friends, easytree.list)
    assert isinstance(tree.context, easytree.dict)
    assert len(tree["context"]) == 2
    assert tree["friends"][0]["age"] == 29


def test_context_manager():
    tree = easytree.dict()
    with tree as t:
        assert t is tree

    tree = easytree.list()
    with tree as t:
        assert t is tree


def test_frozen_dict():
    tree = easytree.dict({"age": 24}, frozen=True)

    with pytest.raises(KeyError):
        tree["name"]

    with pytest.raises(AttributeError):
        tree.name

    with pytest.raises(KeyError):
        tree["name"] = "Bob"

    with pytest.raises(AttributeError):
        tree.name = "Bob"


def test_sealed_dict():
    tree = easytree.dict({"age": 24}, sealed=True)

    with pytest.raises(KeyError):
        tree["name"]

    with pytest.raises(AttributeError):
        tree.name

    with pytest.raises(KeyError):
        tree["name"] = "Bob"

    with pytest.raises(AttributeError):
        tree.name = "Bob"


def test_undefined_value():
    tree = easytree.dict({"age": 29})
    assert isinstance(tree.name, easytree.types.undefined)
    assert isinstance(tree["name"], easytree.types.undefined)


def test_casting():
    assert easytree.types.cast(1) == 1
    assert easytree.types.cast(True) == True
    assert easytree.types.cast("hello world") == "hello world"


def test_attribute_lookup():
    tree = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    assert tree.name == "foo"
    assert tree.address.country == "US"

    with pytest.raises(AttributeError):
        x = tree.numbers.should_not_exists


def test_attribute_assignment():
    tree = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    assert isinstance(tree.numbers, easytree.list)

    tree.numbers.name = "XXX"

    assert isinstance(tree.numbers, easytree.list)
    assert tree.numbers == [1, 3, 5]
    assert tree.numbers != [1, 4, 5]


def test_fromkeys():
    tree = easytree.dict.fromkeys([1, 2, 3], {"hello": "world"})
    assert isinstance(tree, easytree.dict)
    assert isinstance(tree[1], easytree.dict)
    assert len(tree) == 3


def test_update():
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


def test_copy():
    foo = easytree.types.dict({})
    bar = easytree.types.dict(foo)
    assert foo is not bar

    this = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )
    that = easytree.dict(this)

    assert isinstance(that, easytree.dict)

    that.name = "bar"
    assert that.name == "bar"
    assert this.name == "foo"

    this.numbers.append(7)
    assert that.numbers == [1, 3, 5]
    assert this.numbers == [1, 3, 5, 7]

    this.address.country = "France"
    assert this.address.country == "France"
    assert that.address.country == "US"


def test_representation():
    tree = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    assert str(tree) == str(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    assert repr(tree) == repr(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )


def test_appending():
    tree = easytree.list()
    tree.append({"make": "Saab", "color": "blue"})
    tree.append(make="Toyota", color="red")
    tree.append([1, 2, 3])
    tree.append([])
    tree.append([]).append(1)
    tree.append([]).append([1])
    tree.append([]).append([]).append([1])
    tree.append([]).append([]).append([]).append(1)

    assert isinstance(tree, easytree.list)
    assert isinstance(tree[0], easytree.dict)
    assert isinstance(tree[1], easytree.dict)
    assert isinstance(tree[2], easytree.list)
    assert isinstance(tree[3], easytree.list)
    assert isinstance(tree[4], easytree.list)
    assert tree[4] == [1]
    assert tree[5] == [[1]]
    assert tree[6] == [[[1]]]
    assert tree[7] == [[[1]]]

    # appending should return the appended value
    assert tree.append(1) == 1
    assert tree.append([]) == []
    assert isinstance(tree.append([]), easytree.list)
    assert tree.append({}) == {}
    assert isinstance(tree.append({}), easytree.dict)


def test_indexing():
    tree = easytree.list()

    with pytest.raises(IndexError):
        tree[0] = "test"

    tree = easytree.list([1, 2, 3, 4, 5])

    with pytest.raises(TypeError):
        tree["A"]


def test_slicing():
    tree = easytree.list([1, 3, 5, 7])
    assert tree[0:2] == [1, 3]


def test_length():
    tree = easytree.list([1, 2, 3])
    assert len(tree) == 3

    tree = easytree.dict({"name": "David", "age": 29})
    assert len(tree) == 2


def test_iteration():
    for child in easytree.list([1, 2, 3]):
        assert isinstance(child, int)

    for child in easytree.dict({"name": "David", "age": 29}):
        assert isinstance(child, str)

    for item in easytree.list([{}, {}]):
        assert isinstance(item, easytree.dict)


def test_overrides():
    tree = easytree.dict()
    tree.title.text = 1

    assert str(tree) == str({"title": {"text": 1}})

    tree.title = None
    assert str(tree) == str({"title": None})


def test_get():
    tree = easytree.dict()
    assert tree.get("foo") is None
    assert tree.get("foo", "bar") == "bar"

    tree = easytree.dict({"foo": "bar"})
    assert tree.get("foo") == "bar"
    assert tree.get("baz") == None
    assert tree.get("baz", 29) == 29

    tree = easytree.list([1, 3, 5, 6, 7])
    with pytest.raises(AttributeError):
        tree.get("foo")


def test_list_extending():
    tree = easytree.list([0, True])
    tree.extend([1, 2, {}])
    assert len(tree) == 5
    assert isinstance(tree[-1], easytree.dict)

    tree = easytree.list([0, True])
    tree.extend(easytree.list([1, 2, {}]))
    assert len(tree) == 5
    assert isinstance(tree[-1], easytree.dict)


def test_truthfulness():
    tree = easytree.dict()

    if tree:
        raise Exception("An empty dict should be falsy")

    if easytree.dict({"name": "David"}):
        pass
    else:
        raise Exception("An non dict should be falsy")

    if tree.abc:
        raise Exception("An undefined node should be falsy")


def test_mutability():
    tree = easytree.dict({"foo": "bar", "baz": [1, 3, 5, 7, 9]})
    del tree["foo"]
    assert "foo" not in tree

    tree = easytree.dict({"foo": {"bar": "baz"}})
    del tree.foo.bar
    assert "foo" in tree
    assert "baz" not in tree


def test_reverse_update():
    this = {"age": 29, "country": "US"}
    that = easytree.dict({"name": "David", "country": "France"})

    this.update(that)

    assert this == {"name": "David", "age": 29, "country": "France"}


def test_context():
    tree = easytree.dict({"name": "David", "address": {"country": "France"}})

    with tree:
        assert tree.name == "David"

    with tree.address as address:
        assert address.country == "France"


def test_undefined():
    tree = easytree.dict({})
    tree.people.append("Dave")
    assert isinstance(tree.people, list)
    assert len(tree.people) == 1

    tree = easytree.dict({})
    tree.people.append({}).name = "David"
    assert isinstance(tree.people, list)
    assert len(tree.people) == 1

    tree = easytree.dict({})
    tree.people.append({}).name = "David"
    assert isinstance(tree.people, list)
    assert len(tree.people) == 1

    tree = easytree.dict({})
    tree.abc.xyz.append(name="David")
    assert isinstance(tree.abc, dict)
    assert isinstance(tree.abc.xyz, list)
    assert isinstance(tree.abc.xyz[0], dict)


def test_values():
    # dict node
    tree = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    assert isinstance(tree.numbers, list)
    assert list(tree.values()) == ["foo", tree.numbers, tree.address]

    # list node
    tree = easytree.list([1, 2, 3])

    with pytest.raises(AttributeError):
        keys = tree.values()


def test_pop():
    tree = easytree.dict(
        {"name": "Bob", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )
    value = tree.pop("name")
    assert value == "Bob"

    assert tree == {"numbers": [1, 3, 5], "address": {"country": "US"}}

    value = tree.numbers.pop()
    assert value == 5

    assert tree == {"numbers": [1, 3], "address": {"country": "US"}}


def test_inheritence():
    class Grandchild(easytree.dict):
        def walk(self):
            return "walking"

    class Child(easytree.dict):
        def __init__(self, name, age):
            self.adult = age >= 18
            super().__init__({"name": name, "age": age, "grandchild": Grandchild()})

        def own_method(self):
            return True

    instance = Child("Bob", 29)
    instance.address.number = 1
    instance.address.street = "avenue Montaigne"
    instance.address.city = "Paris"
    instance.address.country = "France"

    assert isinstance(instance, Child)
    assert isinstance(instance.address, easytree.dict)
    assert isinstance(instance.grandchild, easytree.dict)

    assert instance.adult == True
    assert instance.own_method() == True

    class Child(easytree.list):
        def append(self, value, *args, **kwargs):
            super().append(value=value, **kwargs)
            return (value, len(args), len(kwargs))

    instance = Child()

    assert isinstance(instance, easytree.list)
    assert isinstance(instance, Child)
    assert instance.append("test") == ("test", 0, 0)
    assert instance.append("test", 1) == ("test", 1, 0)
    assert instance.append("test", name="alpha") == ("test", 0, 1)
    assert instance.append("test", True, name="alpha") == ("test", 1, 1)


def test_deep_get():
    tree = easytree.dict(
        {
            "name": "foo",
            "numbers": [1, 3, {"value": 5, "prime": True}],
            "address": {"country": "US"},
        }
    )

    assert tree.get(["name"]) == "foo"
    assert tree.get([]) is None
    assert tree.get(["numbers", 0]) == 1
    assert tree.get(["numbers", -1, "prime"]) == True
    assert tree.get(["numbers", -1, "odd"]) is None
    assert tree.get(["address", "country"]) == "US"

    assert tree.get(["numbers", 3]) is None
    assert tree.get(["address", "continent"]) is None


def test_pickling():
    this = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    stream = io.BytesIO(pickle.dumps(this))

    that = pickle.load(stream)

    assert isinstance(that, easytree.dict)
    assert isinstance(that.numbers, easytree.list)
    assert isinstance(that.address, easytree.dict)
    assert isinstance(that.address.country, str) and that.address.country == "US"


def test_keys():
    tree = easytree.dict(
        {"name": "foo", "numbers": [1, 3, 5], "address": {"country": "US"}}
    )

    assert all([k in tree.keys() for k in ["name", "numbers", "address"]])

    tree = easytree.list([1, 2, 3])

    with pytest.raises(AttributeError):
        keys = tree.keys()


def test_name_collisions_with_methods():
    tree = easytree.dict({})
    tree.values = 1

    assert tree["values"] == 1
    assert callable(tree.values)  # not to be confused with method...

    setattr(tree, "keys", 2)
    assert tree["keys"] == 2
    assert callable(tree.keys)


def test_appending_nothing_raises():
    x = easytree.list([1, 2, 3])

    with pytest.raises(Exception):
        x.append()


def test_inserting():
    x = easytree.list([1, 2, 3])
    x.insert(1, 4)
    assert x == [1, 4, 2, 3]

    x = easytree.list([1, 2, 3])
    x.insert(3, {"name": "David"})
    assert isinstance(x[-1], easytree.dict)

    x = easytree.list([1, 2, 3])
    x.insert(3, [4, 5, 6])
    assert isinstance(x[-1], easytree.list)

    x = easytree.list([1, 2, 3], frozen=True)
    with pytest.raises(TypeError):
        x.insert(1, 4)

    x = easytree.list([1, 2, 3], sealed=True)
    with pytest.raises(TypeError):
        x.insert(1, 4)


def test_removing():
    x = easytree.list([1, 2, 3])
    x.remove(2)

    assert x == [1, 3]

    x = easytree.list([1, 2, 3], frozen=True)
    with pytest.raises(TypeError):
        x.remove(2)

    x = easytree.list([1, 2, 3], sealed=True)
    with pytest.raises(TypeError):
        x.remove(2)


def test_poping():
    x = easytree.list([1, 2, 3])
    x.pop()

    assert x == [1, 2]

    x = easytree.list([{"name": "Bob"}])
    y = x.pop()

    assert y == {"name": "Bob"}

    x = easytree.list([1, 2, 3], frozen=True)
    with pytest.raises(TypeError):
        x.pop()

    x = easytree.list([1, 2, 3], sealed=True)
    with pytest.raises(TypeError):
        x.pop()


def test_clearing():
    x = easytree.list([1, 2, 3])
    x.clear()

    assert x == []

    x = easytree.list([1, 2, 3], frozen=True)
    with pytest.raises(TypeError):
        x.clear()

    x = easytree.list([1, 2, 3], sealed=True)
    with pytest.raises(TypeError):
        x.clear()


def test_sorting():
    x = easytree.list([2, 1, 3])
    x.sort()

    assert x == [1, 2, 3]

    x = easytree.list([2, 1, 3], sealed=True)
    x.sort()

    assert x == [1, 2, 3]

    x = easytree.list([2, 1, 3], frozen=True)

    with pytest.raises(TypeError):
        x.sort()


def test_copy():
    x = easytree.list([2, 1, 3])
    assert x.copy() is not x
    assert x.copy() == [2, 1, 3]


def test_deleting():
    x = easytree.list([2, 1, 3])
    del x[0]
    assert x == [1, 3]

    x = easytree.list([2, 1, 3], sealed=True)
    with pytest.raises(TypeError):
        del x[1]

    x = easytree.list([2, 1, 3], frozen=True)
    with pytest.raises(TypeError):
        del x[1]

    x = easytree.dict({1: 1, 2: 2, 3: 3})
    del x[1]
    assert x == {2: 2, 3: 3}


def test_setitem():
    x = easytree.list([1, 2, 3])
    x[0] = {"name": "David"}
    assert isinstance(x[0], easytree.dict)


def test_encoding():
    tree = easytree.dict({})
    assert json.dumps(tree) == json.dumps({})

    tree = easytree.list([1, 2, 3])
    assert json.dumps(tree) == json.dumps([1, 2, 3])


def test_recursive_undefined():
    x = easytree.dict()
    x.a.b.c.d.append(True)
    assert x == {"a": {"b": {"c": {"d": [True]}}}}


def test_context_manager():
    profile = easytree.dict()

    with profile.friends.append({"firstname": "Flora"}) as friend:
        friend.birthday = "25/02"
        friend.address.country = "France"

    assert profile.friends[0].birthday == "25/02"


def test_assigning_list_to_undefined():
    value = easytree.dict()
    value.x = [1, 2, 3]

    assert isinstance(value.x, easytree.list)


def test_undefined_does_not_contain():
    value = easytree.dict()
    assert 1 not in value.x


def test_length_of_undefined_is_zero():
    value = easytree.dict()
    assert len(value.x) == 0


def test_cast_optimization():
    x = easytree.list([1, 2, 3])
    assert easytree.types.cast(x) is x

    assert easytree.types.cast(x, sealed=True) is not x
    assert easytree.types.cast(x, frozen=True) is not x

    x = [1, 2, 3]
    assert easytree.types.cast(x) is not x

    x = easytree.dict({"name": "David", "address": {"country": "United States"}})
    assert easytree.types.cast(x) is x
    assert easytree.types.cast(x).address is x.address
    assert easytree.types.cast(x, sealed=True) is not x
    assert easytree.types.cast(x, frozen=True) is not x
    assert easytree.types.cast(x, sealed=True).address is not x.address
    assert easytree.types.cast(x, frozen=True).address is not x.address


def test_subclass_types_are_preserved():
    class A(easytree.list):
        def method_should_exist(self):
            return True

    a = A([1, 2, 3])
    assert isinstance(a, easytree.list)
    assert isinstance(a, A)
    assert isinstance(easytree.types.cast(a), A)
    assert isinstance(easytree.types.cast(a, sealed=True), A)
    assert isinstance(easytree.types.cast(a, frozen=True), A)
    assert easytree.types.cast(a, frozen=True).method_should_exist() is True


def test_nested_subclassing():
    class A(easytree.list):
        def method_should_exist(self):
            return True

    class B(easytree.dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.a = A([])

    b = B(name="David", address={"country": "France"}, x=A([1, 3, 5]))
    assert isinstance(b, easytree.dict)
    assert isinstance(b, B)
    assert isinstance(b.a, A)
    assert isinstance(b.x, A)
    assert b.x.method_should_exist() is True


def test_nested_undefined_writes_multiple():
    x = easytree.dict()
    y = x.y
    y.a = "a"
    y.b = "b"
    y.c = "c"

    assert x.y.a == "a"
    assert x.y.b == "b"
    assert x.y.c == "c"

    x = easytree.dict()
    with x.y as y:
        y.a = "a"
        y.b = "b"
        y.c = "c"

    assert x.y.a == "a"
    assert x.y.b == "b"
    assert x.y.c == "c"

    x = easytree.dict()
    with x.y.z as z:
        z.a = "a"
        z.b = "b"
        z.c = "c"

    assert x.y.z.a == "a"
    assert x.y.z.b == "b"
    assert x.y.z.c == "c"

    x = easytree.dict()
    with x.y.z as z:
        z.a = "a"
        z.b = "b"
        z.c = "c"

    x.y.z = "overwritten"
    assert x.y.z == "overwritten"

    x = easytree.dict()
    with x.y.z as z:
        z.append(1)
        z.append(2)

    assert x.y.z == [1, 2]


def test_undefined_node_cast_as_dict_cannot_append():
    x = easytree.dict()
    with x.y.z as z:
        with pytest.raises(
            TypeError,
        ):
            z.name = "dict node"
            z.append("list node")


def test_undefined_conflict():
    x = easytree.dict()
    with x.y.z as z:
        with pytest.raises(
            TypeError,
        ):
            z.append("list node")
            z.name = "dict node"


def test_undefined_race_conditions():
    x = easytree.dict()
    a = x.y.z
    b = x.y

    assert x == {}

    a.name = "a"
    b.name = "b"

    assert x == {"y": {"z": {"name": "a"}, "name": "b"}}

    x = easytree.dict()
    a = x.y.z
    b = x.y

    assert x == {}


def test_dict_setdefault():
    x = easytree.dict()
    x.a.b.setdefault("c", "this should be set")
    assert x == {"a": {"b": {"c": "this should be set"}}}

    x.a.b.setdefault("c", "this should not be overriden")
    assert x == {"a": {"b": {"c": "this should be set"}}}


def test_dict_setdefault_on_frozen():
    x = easytree.dict(frozen=True)

    with pytest.raises(Exception):
        x.a.b.setdefault("c", "this should raise an error")


def test_dict_setdefault_on_sealed():
    x = easytree.dict(sealed=True)

    with pytest.raises(Exception):
        x.a.b.setdefault("c", "this should raise an error")
