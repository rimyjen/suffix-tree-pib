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