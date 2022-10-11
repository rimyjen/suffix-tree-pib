import os
import sys
from tkinter import W

sys.path.insert(
    1, os.path.join(sys.path[0], "..")
)  # to be able to import modules from parent directory

import pytest
from mccreights import *


@pytest.fixture
def tree():
    x = "ababa"
    yield SuffixTree(x)


def test_fast_scan(tree):
    w = SuffixTreeNode((0, 5), parent=tree.root)
    assert tree.fast_scan(w, 0, 5) == w

    u = tree.fast_scan(w, 0, 3)
    assert u.r == (0, 3)
    assert u.parent == tree.root
    assert u.children == {tree.string[3]: w}
    assert tree.root.children == {tree.string[0]: u}
    assert w.r == (3, 5)
    assert w.parent == u

    v = tree.fast_scan(u, 0, 4)
    assert v.r == (3,4)


