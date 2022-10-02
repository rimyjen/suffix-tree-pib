from helper_functions import *


class SuffixTreeNode:
    def __init__(self, r: tuple[int, int], parent, label=None):
        self.r = r
        self.label: int | None = label
        self.children: dict[str, SuffixTreeNode] = {}
        self.parent: SuffixTreeNode | None = parent

    def __repr__(self):
        return f"SuffixTreeNode({self.r}, {self.label}, {self.parent})"


class SuffixTree:
    def __init__(self, string: str):
        self.root = SuffixTreeNode((0, 0), parent=None)
        self.string = string + "$"

    def __repr__(self):
        return f"SuffixTree({self.string})"

    def find_edge(self, children: dict, key: str) -> SuffixTreeNode:
        """Takes a dictionary and a key. Returns value if key is in dictionary. Otherwise returns None"""
        v = children.get(key)
        return v

    def search_edge(self, v: SuffixTreeNode, j: int) -> int:
        """Takes a node and a suffix index. Returns number of comparisons made before mismatch or edge end"""
        return search_range(self.string, v.r, self.string, j)

    def search_path(self, v: SuffixTreeNode, j: int) -> tuple[SuffixTreeNode, int]:
        """
        Takes a node and an index. Recursively searches suffix tree.
        Returns position of mismatch given by a node and the number of steps taken towards that node.
        """
        out = self.find_edge(v.children, self.string[j])
        if out is None:
            return v, 0
        length = self.search_edge(out, j)
        if j + length == len(
            self.string
        ):  # j + length is end of string we search for. In case of no sentinel.
            raise Exception("Reached end of suffix string with no mismatches")
        if length < range_length(out.r[0], out.r[1]):
            return out, length
        return self.search_path(out, j + length)

    def split_edge(self, v: SuffixTreeNode, k: int) -> SuffixTreeNode:
        """
        Takes position of mismatch given as a node and and the number of steps taken towards that node.
        Returns new internal node at given position.
        """
        p = v.parent
        i, n = v.r

        u = SuffixTreeNode((i, i + k), parent=p)
        add_to_dictionary(u.children, self.string[i + k], v)
        add_to_dictionary(p.children, self.string[i], u)

        v.r = (i + k, n)
        v.parent = u

        return u

    def insert_child(self, u: SuffixTreeNode, j: int) -> SuffixTreeNode:
        """Takes an internal node and a suffix index. Inserts leaf node as child of internal node. Returns leaf node"""
        x = j + range_length(u.r[0], u.r[1])
        leaf = SuffixTreeNode((x, len(self.string)), parent=u, label=j)
        add_to_dictionary(u.children, self.string[x], leaf)
        return leaf

    def naive_insert(self):
        """Iteratively inserts suffixes in suffix tree"""
        for j in range(len(self.string)):
            v, k = self.search_path(self.root, j)
            if k > 0:
                u = self.split_edge(v, k)
            else:
                u = v
            self.insert_child(u, j)


test = SuffixTree("abbaa")
test.naive_insert()
print(test)
