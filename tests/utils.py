import pytest
import easytree


def test_frozen():
    tree = easytree.dict(frozen=True)
    assert easytree.frozen(tree) is True

    tree = easytree.dict(frozen=False)
    assert easytree.frozen(tree) is False

    tree = easytree.list(frozen=True)
    assert easytree.frozen(tree) is True

    tree = easytree.list(frozen=False)
    assert easytree.frozen(tree) is False

    with pytest.raises(TypeError):
        assert easytree.frozen(False)


def test_freeze():
    tree = easytree.dict()
    assert easytree.frozen(tree) is False
    assert easytree.frozen(easytree.freeze(tree)) is True

    tree = easytree.list()
    assert easytree.frozen(easytree.freeze(tree)) is True

    tree = easytree.dict({"person": {"firstname": "David"}})
    assert easytree.frozen(easytree.freeze(tree).person) is True

    tree = easytree.dict({"friends": [{"firstname": "David"}]})
    assert easytree.frozen(easytree.freeze(tree).friends) is True
    assert easytree.frozen(easytree.freeze(tree).friends[0]) is True

    tree = easytree.dict({"friends": [{"firstname": "David"}]}, frozen=True)
    with pytest.raises(Exception):
        tree.friends.append({"firstname": "Bob"})

    tree = easytree.list([1, 2, 3], frozen=True)
    with pytest.raises(Exception):
        tree.extend([4, 5, 6])


def test_unfreeze():
    tree = easytree.dict(frozen=True)
    assert easytree.frozen(tree) is True
    assert easytree.frozen(easytree.unfreeze(tree)) is False

    tree = easytree.list(frozen=True)
    assert easytree.frozen(tree) is True
    assert easytree.frozen(easytree.unfreeze(tree)) is False

    tree = easytree.dict({"person": {"firstname": "David"}}, frozen=True)
    assert easytree.frozen(easytree.unfreeze(tree).person) is False

    tree = easytree.dict({"friends": [{"firstname": "David"}]}, frozen=True)
    assert easytree.frozen(easytree.unfreeze(tree).friends) is False
    assert easytree.frozen(easytree.unfreeze(tree).friends[0]) is False


def test_sealed():
    tree = easytree.dict(sealed=True)
    assert easytree.sealed(tree) is True

    tree = easytree.dict(sealed=False)
    assert easytree.sealed(tree) is False

    tree = easytree.list(sealed=True)
    assert easytree.sealed(tree) is True

    tree = easytree.list(sealed=False)
    assert easytree.sealed(tree) is False

    with pytest.raises(TypeError):
        assert easytree.sealed(False)


def test_sealing():
    tree = easytree.dict()
    assert easytree.sealed(tree) is False
    assert easytree.sealed(easytree.seal(tree)) is True

    tree = easytree.list()
    assert easytree.sealed(easytree.seal(tree)) is True

    tree = easytree.dict({"person": {"firstname": "David"}})
    assert easytree.sealed(easytree.seal(tree).person) is True

    tree = easytree.dict({"friends": [{"firstname": "David"}]})
    assert easytree.sealed(easytree.seal(tree).friends) is True
    assert easytree.sealed(easytree.seal(tree).friends[0]) is True

    tree = easytree.dict({"friends": [{"firstname": "David"}]}, sealed=True)

    with pytest.raises(Exception):
        tree.friends.append({"firstname": "Bob"})

    tree.friends[0].firstname = "Bob"
    assert tree.friends[0].firstname == "Bob"


def test_unsealing():
    tree = easytree.dict(sealed=True)
    assert easytree.sealed(tree) is True
    assert easytree.sealed(easytree.unseal(tree)) is False

    tree = easytree.list(sealed=True)
    assert easytree.sealed(tree) is True
    assert easytree.sealed(easytree.unseal(tree)) is False

    tree = easytree.dict({"person": {"firstname": "David"}}, sealed=True)
    assert easytree.sealed(easytree.unseal(tree).person) is False

    tree = easytree.dict({"friends": [{"firstname": "David"}]}, sealed=True)
    assert easytree.sealed(easytree.unseal(tree).friends) is False
    assert easytree.sealed(easytree.unseal(tree).friends[0]) is False
