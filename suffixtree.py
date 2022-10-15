import graphviz


class SuffixTreeNode:
    def __init__(self, r, parent, label=None):
        self.r: tuple[int, int] = r
        self.label: int | None = label
        self.children: dict[str, SuffixTreeNode] = {}
        self.parent: SuffixTreeNode | None = parent

    def __repr__(self):
        return f"SuffixTreeNode({self.r}, label = {self.label})"

    def find_child(self, key: str):
        """Takes a dictionary and a key. Returns value if key is in dictionary. Otherwise returns None"""
        return self.children.get(key)

    def add_child(self, key: str, value):
        self.children[key] = value

    def get_edge_length(self) -> int:
        return self.r[1] - self.r[0]

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
    def __init__(self, root: SuffixTreeNode, string: str):
        self.root = root
        self.string = string

    def __repr__(self):
        return f"SuffixTree({self.string})"

    def to_dot(self):
        return 'digraph { rankdir="LR" ' + "\n".join(self.root.to_dot()) + "}"

    def to_graphviz(self):
        graph = self.to_dot()
        return graphviz.Source(graph)


def search_edge(x: str, v: SuffixTreeNode, j: int) -> int:
    """Takes a string, a node and a suffix index. Returns number of comparisons made between node edge and suffix before mismatch or edge end"""
    i, m = v.r
    length = min(m - i, len(x) - j)
    for k in range(length):
        if x[i + k] != x[j + k]:
            return k
    return length


def search_path(x: str, v: SuffixTreeNode, j: int) -> tuple[SuffixTreeNode, int]:
    """
    Takes a node and an index. Recursively searches suffix tree.
    Returns position of mismatch given by a node and the number of steps taken towards that node.
    """
    out = v.find_child(x[j])
    if out is None:
        return v, 0
    length = search_edge(x, out, j)
    if j + length == len(x):
        # j + length is end of string we search for. In case of no sentinel.
        raise Exception("Reached end of suffix string with no mismatches")
    if length < out.get_edge_length():
        return out, length
    return search_path(x, out, j + length)


def split_edge(x: str, v: SuffixTreeNode, k: int) -> SuffixTreeNode:
    """
    Takes position of mismatch given as a node and and the number of steps taken towards that node.
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


def insert_child(x: str, u: SuffixTreeNode, j: int) -> SuffixTreeNode:
    """Takes an internal node and a suffix index. Inserts leaf node as child of internal node. Returns leaf node"""
    k = j + u.get_edge_length()
    leaf = SuffixTreeNode((k, len(x)), parent=u, label=j)
    u.add_child(x[k], leaf)
    return leaf


def naive_st_construction(x: str) -> SuffixTree:
    """Iteratively inserts suffixes in suffix tree"""
    x = x + "$"
    root = SuffixTreeNode((0, 0), parent=None)

    for j in range(len(x)):
        v, k = search_path(x, root, j)
        if k > 0:
            u = split_edge(x, v, k)
        else:
            u = v
        insert_child(x, u, j)

    return SuffixTree(root, x)


tree = naive_st_construction("ABABB")
print(tree)

graph = tree.to_graphviz()
graph.render("graphviz/suffixtree", view=False)
