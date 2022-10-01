from helper_functions import *

class SuffixTreeNode:
    def __init__(self, r: tuple[int,int], parent, label = None):
        self.r = r
        self.label = label
        self.children:dict[str, SuffixTreeNode] = {}
        self.parent:SuffixTreeNode|None = parent

    def __repr__(self):
        return f'SuffixTreeNode({self.r}, {self.label}, {self.parent})'
        
class SuffixTree:
    def __init__(self, string: str):
        self.root = SuffixTreeNode((0,0), parent = None)
        self.string = string

    def __repr__(self):
        return f'SuffixTree({self.string})'

    def find_edge(self, children: dict, key: str) -> SuffixTreeNode:
        '''Takes a dictionary and a key. Returns value if key is in dictionary. Otherwise returns None'''
        v = children.get(key)
        return v

    def search_edge(self, v: SuffixTreeNode, j: int) -> int:
        '''Takes a node and a suffix index. Returns number of comparisons made before mismatch or edge end'''
        return search_range(self.string, v.r, self.string, j)

    def search_path(self, v: SuffixTreeNode, j: int) -> tuple[SuffixTreeNode, int]:
        '''
        Takes a node and an index. Recursively searches suffix tree. 
        Returns position of mismatch given by a node and the number of steps taken towards that node.
        '''
        out = self.find_edge(v.children, self.string[j])
        if out is None:
            return v, 0
        length = self.search_edge(out, j)
        if j + length == len(self.string): # j + length is end of string we search for. In case of no sentinel.
            raise Exception("Reached end of suffix string with no mismatches")
        if length < out.r[1]-out.r[0]:
            return out, length
        return self.search_path(out, j + length)

    def split_edge(self, v: SuffixTreeNode, j: int) -> SuffixTreeNode:
        '''Takes position of mismatch given as a node and an index. Returns new internal node at given position'''
        p = v.parent
        i,n = v.r
        
        u = SuffixTreeNode((i, j), parent = p)
        u.children[self.string[j]] = v

        p.children[self.string[i]] = u

        v.r = (j, n)
        v.parent = u

        return u

    def insert_child():
        '''Creates a new leaf node and inserts it as a child of a parent node'''
        pass

    def naive_insert():
        '''Takes root and string. Returns suffix tree'''
        pass