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
        child = children.get(key)
        return child

    def search_edge(self, v: SuffixTreeNode, j: int) -> int:
        '''Takes a node and a suffix index. Returns index of mismatch or edge end.'''
        return search_range(self.string, v.r, self.string, j)

    def search_path(self, v: SuffixTreeNode, j: int) -> tuple[SuffixTreeNode, int]:
        out = self.find_edge(v.children, self.string[j])
        if out is None:
            return v, 0 # Or v.range[1]-v.range[0]
        length = self.search_edge(out, j)
        # Something bad can happen here without sentinel.
        if j + length == len(self.string): # j + length is end of string we search for
            return out, length
        return self.search_path(out, j + length)

    def split_edge():
        '''
        Splits edge at mismatch position
        Creates internal node by updating children
        Returns the new internal node'''
        pass

    def insert_child():
        '''Creates a new leaf node and inserts it as a child of a parent node'''
        pass

    def naive_insert():
        '''Takes root and string. Returns suffix tree'''
        pass