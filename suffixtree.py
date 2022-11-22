import graphviz


class SuffixTreeNode:
    def __init__(self, r, parent=None, suffix_link=None, label=None):
        self.r: tuple[int, int] = r
        self.label: int | None = label
        self.children: dict[str, SuffixTreeNode] = {}
        self.parent: SuffixTreeNode | None = parent
        self.suffix_link: SuffixTreeNode | None = suffix_link

    def __repr__(self):
        return f"SuffixTreeNode({self.r}, label = {self.label})"

    def __iter__(self):
        for key in self.children:
            child = self.children[key]

            if child.label == None:
                yield from child
            else:
                yield child

    def find_child(self, key: str):
        """Takes a dictionary and a key. Returns value if key is in dictionary. Otherwise returns None"""
        return self.children.get(key)

    def add_child(self, key: str, value):
        self.children[key] = value

    def get_edge_length(self) -> int:
        return self.r[1] - self.r[0]

    def to_dot(self, tree):
        if self.parent is None:
            yield f'{id(self)}[label = "", shape = circle, style = filled, fillcolor = grey]'
        else:
            if self.label is None:
                yield f'{id(self)}[label = "", shape = circle, style = filled, fillcolor = grey]'
            else:
                yield f"{id(self)}[label = {self.label}, shape = circle, style = filled, fillcolor = grey]"
            label = f'{tree.string[slice(*self.r)]} ({",".join(map(str, self.r))})'
            yield f'{id(self.parent)} -> {id(self)}[label = "{label}"]'

        for key in self.children:
            child = self.children[key]
            yield from child.to_dot(tree)


class SuffixTree:
    def __init__(self, root: SuffixTreeNode, string: str):
        self.root = root
        self.string = string
        self.root.suffix_link = self.root

    def __repr__(self):
        return f"SuffixTree({self.string})"

    def to_dot(self):
        return 'digraph { rankdir="LR" ' + "\n".join(self.root.to_dot(self)) + "}"

    def to_graphviz(self):
        graph = self.to_dot()
        return graphviz.Source(graph)


def search_edge(x: str, v: SuffixTreeNode, y: str, j: int) -> int:
    """
    Takes a string x and a SuffixTreeNode v containing a range to search in the string.
    Takes another string y and an index j specifying where in the string to search from.
    Returns number of comparisons made between the two strings before mismatch or end of string x.
    Requires string y to end with a sentinel.
    Without sentinel function fails to distinguish if end of string x or y was reached.
    """
    i, m = v.r
    length = min(m - i, len(y) - j)
    for k in range(length):
        if x[i + k] != y[j + k]:
            return k
    return length


def search_path(
    x: str, v: SuffixTreeNode, j: int, d: int, y: str | None = None
) -> tuple[SuffixTreeNode, int]:
    """
    Takes a string, a node, an index and a distance to the root.
    Recursively searches suffix tree.
    Returns position of mismatch given by a node, the number of steps taken towards that node, and the distance to the root.
    """
    y = y if y is not None else x
    out = v.find_child(y[j])
    if out is None:
        return v, 0, d
    length = search_edge(x, out, y, j)
    if j + length == len(x):
        # j + length is end of string we search for. In case of no sentinel.
        raise Exception(
            "Reached end of suffix with no mismatches. Make sure string contains sentinel."
        )
    if length < out.get_edge_length():
        return out, length, d + length
    if j + length == len(y):
        return out, length, d + length
    return search_path(x, out, j + length, d + length, y)


def split_edge(x: str, v: SuffixTreeNode, k: int) -> SuffixTreeNode:
    """
    Takes position of mismatch given as a node and the number of steps taken towards that node.
    Returns new internal node at given position.
    """
    p = v.parent
    i, n = v.r

    u = SuffixTreeNode((i, i + k), parent=p)
    u.add_child(x[i + k], v)
    p.add_child(x[i], u)

    v.r = (i + k, n)
    v.parent = u

    return u


def insert_child(x: str, u: SuffixTreeNode, j: int, d: int) -> SuffixTreeNode:
    """
    Takes a string, an internal node, a suffix index and distance to root.
    Inserts leaf node as child of internal node.
    Returns leaf node
    """
    leaf = SuffixTreeNode((j + d, len(x)), parent=u, label=j)
    u.add_child(x[j + d], leaf)
    return leaf


def naive_st_construction(x: str) -> SuffixTree:
    """Iteratively inserts suffixes in suffix tree"""
    x = x + "$"
    root = SuffixTreeNode((0, 0))

    for j in range(len(x)):
        v, k, d = search_path(x, root, j, 0)
        if k > 0:
            u = split_edge(x, v, k)
        else:
            u = v
        insert_child(x, u, j, d)

    return SuffixTree(root, x)


def fast_scan(x: str, w: SuffixTreeNode, i: int, j: int) -> SuffixTreeNode:
    """
    Takes a node w and a range from i to j. I.e. compares two strings, and jumps from node to node.
    Invariants:
        j-i > 0
    3 cases:
        1. The two strings match. Return node
        2. len(w.r) > j-i. Create new node at w.r[0] + j-i. Return new node.
        3. len(w.r) < j-i. Recurse until case 1 or 2.
            1. Find new edge to search from with find_child. Update i = i + len(w.r). Update w.
            2. fast_scan(new_w, new_i, y)
    """

    length_w = w.get_edge_length()
    length_ij = j - i

    assert length_ij > 0

    if length_w > length_ij:
        return split_edge(x, w, length_ij)
        # return "length_w > length_ij"
    elif length_w < length_ij:
        i += length_w
        out = w.find_child(x[i])
        return fast_scan(x, out, i, j)
    else:
        return w


def suffix_search(x: str, v: SuffixTreeNode, root: SuffixTreeNode) -> SuffixTreeNode:
    """
    Takes parent v of last leaf i-1. Returns node from where to start naive_scan.
    4 cases:
        1. v is root. Return root
        2. v is child of root & v.get_edge_length() == 1. Return root
        3. v is child of root & v.get_edge_length() > 1. Fast_scan(root, (v.r[0]+1, v.r[1]))   # check first if v has suffix link
        4. v is not child of root. Fast_scan(v.parent.suffixlink.child, v.r)  # check first if v has suffix link
    """
    if v == root:
        return root

    elif v.parent == root:
        length = v.get_edge_length()
        assert length > 0

        if length == 1:
            return root

        else:
            return fast_scan(x, root, v.r[0] + 1, v.r[1])

    else:
        s = v.parent.suffix_link
        assert s is not None, "No suffix link present"
        w = s.find_child(x[v.r[0]])
        return fast_scan(x, w, v.r[0], v.r[1])


def mccreights_st_construction(x: str) -> SuffixTree:
    """
    Iterate over suffixes x[i,n]$ for i in range(1,n).
        1. Get parent v of last leaf i-1.
        2. Suffix_search(v) returns node w.
        3. Set suffix link of v to w.
        4. From w, use naive_scan to find h(i).
        5. Make internal node, if not already
        6. Insert t(i) as child of h(i)
    """
    x = x + "$"
    root = SuffixTreeNode((0, 0))
    leaf = insert_child(x, root, 0, 0)
    v = leaf.parent

    for i in range(1, len(x)):
        if v.suffix_link == None:
            w = suffix_search(x, v, root)
            v.suffix_link = w

        else:
            w = v.suffix_link

        if w == root:
            h, k, d = search_path(x, w, i, 0)
        else:
            h, k, d = search_path(x, w, leaf.r[0], d - 1)

        if k > 0:
            u = split_edge(x, h, k)
        else:
            u = h

        leaf = insert_child(x, u, i, d)
        v = leaf.parent

    return SuffixTree(root, x)


tree = mccreights_st_construction("abbaba")
graph = tree.to_graphviz()
graph.render("graphviz/suffixtree_mccr", view=False)
