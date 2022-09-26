class SuffixTreeNode:
    def __init__(self, range, label = None):
        self.range = range
        self.label = label
        self.children = {}

    def __repr__(self):
        return f'SuffixTreeNode({self.range}, "{self.label}")'
        
class SuffixTree:
    def __init__(self, string):
        self.root = SuffixTreeNode((0,0))
        self.string = string

    def __repr__(self):
        return f'SuffixTree("{self.string}")'

    def find_edge(self, children, key):
        '''Takes a dictionary and a key. Returns value if key is in dictionary. Otherwise returns None'''
        child = children.get(key)
        return child

    def search_edge():
        '''Should look through edge until end or mismatch'''
        pass

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