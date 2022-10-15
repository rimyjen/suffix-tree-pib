import os
import sys

# to be able to import modules from parent directory
sys.path.insert(1, os.path.join(sys.path[0], ".."))

import pytest
from suffixtree import *


##################################
# TESTING CONSTRUCTION FUNCTIONS #
##################################


@pytest.mark.parametrize("key, expected_value", [("a", "child1"), ("b", None)])
def test_find_child(key, expected_value):
    v = SuffixTreeNode((0, 0), parent=None)
    v.add_child("a", "child1")
    assert v.find_child(key) == expected_value


@pytest.mark.parametrize(
    "x, v, y, j, expected_value",
    [
        ("", SuffixTreeNode((0, 0)), "", 0, 0),
        ("a", SuffixTreeNode((0, 1)), "", 0, 0),
        ("", SuffixTreeNode((0, 0)), "a", 0, 0),
        ("a", SuffixTreeNode((0, 1)), "a", 0, 1),
        ("b", SuffixTreeNode((0, 1)), "a", 0, 0),
        ("ab", SuffixTreeNode((0, 2)), "a", 0, 1),
        ("a", SuffixTreeNode((0, 1)), "ab", 0, 1),
        ("ab", SuffixTreeNode((1, 2)), "b", 0, 1),
        ("ab", SuffixTreeNode((1, 2)), "ab", 1, 1),
    ],
)
def test_search_edge(x, v, y, j, expected_value):
    assert search_edge(x, v, y, j) == expected_value


def test_search_path():
    x = "ababa$"
    root = SuffixTreeNode((0, 0))
    v = SuffixTreeNode((0, 3), parent=root)
    leaf = SuffixTreeNode((3, 6), parent=v, label=0)
    v.children[x[3]] = leaf
    root.children[x[0]] = v

    # no mismatches in suffix should raise exception:
    with pytest.raises(Exception) as excinfo:
        search_path(x, root, 0)
    assert "Reached end" in str(excinfo.value)
    # no matching children in root:
    assert search_path(x, root, 1) == (root, 0)
    # no matching children after reaching internal root:
    assert search_path(x, root, 2) == (v, 0)
    # mismatch:
    assert search_path(x, root, 4) == (v, 1)
    # starting search from internal node:
    assert search_path(x, v, 4) == (v, 0)


def test_split_edge():
    x = "ababa$"
    root = SuffixTreeNode((0, 0))
    leaf = SuffixTreeNode((0, 6), parent=root, label=0)
    root.children[x[0]] = leaf
    v = split_edge(x, leaf, 3)

    assert v.r == (0, 3)
    assert v.parent == root
    assert v.children == {x[3]: leaf}
    assert root.children == {x[0]: v}
    assert leaf.r == (3, 6)
    assert leaf.parent == v


def test_insert_child():
    x = "ababa$"
    root = SuffixTreeNode((0, 0))
    v = SuffixTreeNode((1, 3), parent=root)
    leaf = SuffixTreeNode((3, 6), parent=v, label=0)
    v.children[x[3]] = leaf
    root.children[x[1]] = v
    new_leaf = insert_child(x, v, 3)

    assert new_leaf.r == (5, 6)
    assert new_leaf.parent == v
    assert new_leaf.label == 3
    assert v.children[x[new_leaf.r[0]]] == new_leaf


##################################
# GENERAL TESTING OF SUFFIX TREE #
##################################


@pytest.fixture
def naive_tree():
    yield naive_st_construction("ababb")


def test_suffix_indexes_in_tree(naive_tree):
    """
    Compares list of expected leaf labels to leaf labels in tree.
    During this test incode assert statements also test:
    1. internal nodes have > 1 child
    2. leaf nodes have 0 children
    """
    suffix_indexes = list(range(len(naive_tree.string)))

    leaf_labels = []
    for val in iter(naive_tree.root):
        leaf_labels.append(val.label)
    leaf_labels.sort()

    assert suffix_indexes == leaf_labels


def test_suffixes_are_correct(naive_tree):
    """Tests if all suffixes are represented in the tree as expected, by concatenating edged from leafs to root"""

    l = []
    for val in iter(naive_tree.root):
        node = val
        s = []
        while node.parent != None:
            i, j = node.r
            s.append(naive_tree.string[i:j])
            node = node.parent
        s.reverse()
        suffix = "".join(s)
        l.append(suffix)

    for i in range(len(naive_tree.string)):
        assert naive_tree.string[i:] in l
