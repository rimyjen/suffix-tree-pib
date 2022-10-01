import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) #to be able to import modules from parent directory

import pytest
from naive import *

@pytest.fixture
def string():
    yield "ababa$"

@pytest.fixture
def tree(string):
    yield SuffixTree(string)

@pytest.mark.parametrize(
    'key, expected_value',
    [('a', 'child1'), ('b', None)])

def test_find_edge(key, expected_value, tree): 
    assert tree.find_edge({'a': 'child1'}, key) == expected_value

def test_search_edge(tree):
    assert tree.search_edge(tree.root, 3) == 0
    assert tree.search_edge(SuffixTreeNode((1,3), parent = tree.root), 3) == 2
    assert tree.search_edge(SuffixTreeNode((0,6), parent = tree.root), 4) == 1

def test_search_path(string):
    x = string
    tree = SuffixTree(x)
    v = SuffixTreeNode((0,3), parent = tree.root)
    leaf = SuffixTreeNode((3,6), parent = v, label = 0)
    v.children[x[3]] = leaf
    tree.root.children[x[0]] = v

    with pytest.raises(Exception) as excinfo: #no mismatches in suffix 
        tree.search_path(tree.root, 0)
    assert "Reached end" in str(excinfo.value)

    assert tree.search_path(tree.root, 1) == (tree.root, 0) #no matching children in root
    assert tree.search_path(tree.root, 2) == (v, 0) #no matching children after reaching internal node
    assert tree.search_path(tree.root, 4) == (v, 1) #mismatch
    
def test_split_edge(string):
    x = string
    tree = SuffixTree(x)
    v = SuffixTreeNode((0,6), parent = tree.root, label = 0)
    tree.root.children[x[0]] = v
    u = tree.split_edge(v, 3)

    assert u.r == (0,3)
    assert u.parent == tree.root
    assert u.children == {x[3]: v}
    assert tree.root.children == {x[0]: u}
    assert v.r == (3,6)
    assert v.parent == u

def test_insert_child(string):
    x = string
    tree = SuffixTree(x)
    u = SuffixTreeNode((0,3), parent = tree.root)
    v = SuffixTreeNode((3,6), parent = u, label = 0)
    u.children[x[3]] = v
    tree.root.children[x[0]] = u

    leaf = tree.insert_child(u, 2)
    assert leaf.r == (5,6)
    assert leaf.parent == u
    assert leaf.label == 2
    assert u.children[x[leaf.r[0]]] == leaf