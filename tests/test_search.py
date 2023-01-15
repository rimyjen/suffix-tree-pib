import os
import sys

# to be able to import modules from parent directory
sys.path.insert(1, os.path.join(sys.path[0], ".."))

import pytest
from suffixtree import *
from search import *


@pytest.mark.parametrize(
    "y, expected_output",
    [
        ("mississippi", [0]),
        ("i", [1, 4, 7, 10]),
        ("x", []),
        ("ssi", [2, 5]),
        ("mississippis", []),
    ],
)
def test_find_occurrences(y, expected_output):  # , y: str, expected_output
    tree = mccreights_st_construction("mississippi")
    l = []
    for leaf in find_occurrences(tree, y):
        l.append(leaf.label)

    assert l == expected_output

