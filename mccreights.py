import graphviz
from helper_functions import *


class SuffixTreeNode:
    def __init__(self, r: tuple[int, int], parent, suffix_link=None, label=None):
        self.r = r
        self.label: int | None = label
        self.children: dict[str, SuffixTreeNode] = {}
        self.parent: SuffixTreeNode | None = parent
        self.suffix_link: SuffixTreeNode | None = suffix_link

    def __repr__(self):
        return (
            f"SuffixTreeNode({self.r}, {self.parent}, {self.suffix_link}, {self.label})"
        )

    def find_child(self, key: str):
        """Takes a dictionary and a key. Returns value if key is in dictionary. Otherwise returns None"""
        return self.children.get(key)

    def add_child(self, key: str, value):
        self.children[key] = value

    def get_edge_length(self) -> int:
        return get_range_length(self.r[0], self.r[1])

    def to_dot(self):
        if self.parent is None:
            yield f'{id(self)}[label = "", shape = circle, style = filled, fillcolor = grey]'
        else:
            if self.label is None:
                yield f'{id(self)}[label = "", shape = circle, style = filled, fillcolor = grey]'
            else:
                yield f"{id(self)}[label = {self.label}, shape = circle, style = filled, fillcolor = grey]"
            label = f'({",".join(map(str, self.r))})'
            yield f'{id(self.parent)} -> {id(self)}[label = "{label}"]'

        for key in self.children:
            child = self.children[key]
            yield from child.to_dot()


class SuffixTree:
    def __init__(self, string: str):
        self.root = SuffixTreeNode((0, 0), parent=None)
        self.string = string + "$"
        self.root.suffix_link = self.root
        self.insert_child(self.root, 0)

    def __repr__(self):
        return f"SuffixTree({self.string})"

    def search_edge(self, v: SuffixTreeNode, j: int) -> int:
        """Takes a node and a suffix index. Returns number of comparisons made before mismatch or edge end"""
        return search_range(self.string, v.r, self.string, j)

    def split_edge(self, v: SuffixTreeNode, k: int) -> SuffixTreeNode:
        """
        Takes position of mismatch given as a node and and the number of steps taken towards that node.
        Returns new internal node at given position.
        """
        p = v.parent
        i, n = v.r

        u = SuffixTreeNode((i, i + k), parent=p)
        u.add_child(self.string[i + k], v)
        p.add_child(self.string[i], u)

        v.r = (i + k, n)
        v.parent = u

        return u

    def insert_child(self, u: SuffixTreeNode, j: int) -> SuffixTreeNode:
        """Takes an internal node and a suffix index. Inserts leaf node as child of internal node. Returns leaf node"""
        x = j + u.get_edge_length()
        leaf = SuffixTreeNode((x, len(self.string)), parent=u, label=j)
        u.add_child(self.string[x], leaf)
        return leaf

    def naive_scan(self):
        """
        Uses search_edge to search for h(i) by looking at one character at a time.
        Two cases:
            1. h(i-1) is empty. Start from root.
            2. h(i-1) is not empty. Start from internal node w.
        """
        pass

    def fast_scan(self, w: SuffixTreeNode, x: int, y: int) -> SuffixTreeNode:
        """
        Takes a node w and a range x, y. I.e. compares two strings, and jumps from node to node.
        Invariants:
            len(w.r), len(x,y) > 0
            self.string[w.r[0]] == self.string[x]
        3 cases:
            1. The two strings match. Return node
            2. len(w.r) > len(x,y). Create new node at w.r[0] + len(x,y). Return new node.
            3. len(w.r) < len(x,y). Recurse until case 1 or 2.
                1. Find new edge to search from with find_child. Update x = x + len(w.r). Update w.
                2. fast_scan(new_w, new_x, y)
        """
        length_w = w.get_edge_length()
        length_xy = get_range_length(x, y)
        # assert invariants
        if length_w > length_xy:
            out = self.split_edge(w, length_xy)
            return out
        elif length_w < length_xy:
            # this part doesn't work, attribute error, 'Nonetype'
            x += length_w
            out = w.find_child(self.string[x])
            self.fast_scan(out, x, y)
        else:
            return w

    def suffix_search(self, v):
        """
        Takes parent v of last leaf i-1. Returns node from where to start naive_scan.
        4 cases:
            1. v is root. Return root
            2. v is child of root & v.get_range_length() == 1. Return root
            3. v is child of root & v.get_range_length() > 1. Fast_scan(root, (v.r[0]+1, v.r[1]))
            4. v is not child of root. Fast_scan(v.parent.suffixlink, v.r)
        """
        pass

    def mccreights(self):
        """
        Iterate over suffixes x[i,n]$ for i in range(1,n).
            1. Get parent v of last leaf i-1.
            2. Suffix_search(v) returns node w.
            3. Set suffix link of v to w.
            4. From w, use naive_scan to find h(i). h(i) is a node
            5. Insert t(i) as child of h(i)
        """
        pass

    def to_dot(self):
        return 'digraph { rankdir="LR" ' + "\n".join(self.root.to_dot()) + "}"

    def to_graphviz(self):
        graph = self.to_dot()
        return graphviz.Source(graph)


test = SuffixTree("MISSISSIPPI")

graph = test.to_graphviz()
graph.render("graphviz/mccreights", view=False)
