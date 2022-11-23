from suffixtree import *
from tests import test_suffixtree as funcs
from typing import Iterator

##########################
# Exact Pattern Matching #
##########################


def find_occurrences(tree: SuffixTree, y: str) -> Iterator[int]:
    out, _, prefix_len = search_path(tree.string, tree.root, j=0, d=0, y=y)
    if prefix_len == len(y):
        yield from out


def matches(y: str):
    print("searching for:", y)
    for leaf in find_occurrences(tree, y):
        print(tree.string[leaf.label :])
    print("done")
    print()


####################
# Locating Repeats #
####################


def print_vals_from_lists(a, b):
    for i in a:
        for j in b:
            print(i, j)


def get_internal_nodes(tree):
    s = set()
    for node in iter(tree.root):
        p = node.parent
        while p is not None:
            if p.parent is not None:
                s.add(p)
            p = p.parent
    return s


def get_subtrees_from_node(v):
    """Create list with lists of leaf nodes for each subtree of an internal nodes"""
    children = v.children
    d = []
    for key in children:
        l = []
        if children[key].label is not None:
            l.append(children[key].label)
        for j in iter(children[key]):
            l.append(j.label)
        d.append(l)
    return d


def find_right_maximal_repeats(v):
    subtrees = get_subtrees_from_node(v)
    print("Repeat:", funcs.get_path_label(tree.string, v))
    # assuming all repeats start from the root

    for i in range(len(subtrees) - 1):
        for j in range(i+1, len(subtrees)):
            print_vals_from_lists(subtrees[i], subtrees[j])

tree = mccreights_st_construction("mississippi")
graph = tree.to_graphviz()
graph.render("graphviz/suffixtree_mccr", view=False)

for v in get_internal_nodes(tree):
    find_right_maximal_repeats(v)
