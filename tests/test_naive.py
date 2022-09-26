import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..')) #to be able to import modules from parent directory

import pytest
from naive import *

@pytest.fixture
def Tree():
    return SuffixTree("abaaba")

def test_always_passes():
    assert True

def test_always_fails():
    assert False

def test_find_edge(Tree): 
    assert Tree.find_edge({"a": "child1"}, "a") == "child1"

def test_no_edge(Tree):
    assert Tree.find_edge({}, "x") == None
