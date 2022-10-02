import os
import sys

sys.path.insert(
    1, os.path.join(sys.path[0], "..")
)  # to be able to import modules from parent directory

import pytest
from helper_functions import *


@pytest.mark.parametrize(
    "x, r, y, j, expected_value",
    [
        ("", (0, 0), "", 0, 0),
        ("a", (0, 1), "", 0, 0),
        ("", (0, 0), "a", 0, 0),
        ("a", (0, 1), "a", 0, 1),
        ("b", (0, 1), "a", 0, 0),
        ("ab", (0, 2), "a", 0, 1),
        ("a", (0, 1), "ab", 0, 1),
        ("ab", (1, 2), "b", 0, 1),
        ("ab", (1, 2), "ab", 1, 1),
    ],
)
def test_search_range(x, r, y, j, expected_value) -> None:
    assert search_range(x, r, y, j) == expected_value
