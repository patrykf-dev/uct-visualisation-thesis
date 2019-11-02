import os


class Tree:
    def __init__(self, node="", *children):
        self.node = node
        self.width = len(node)
        if children:
            self.children = children
        else:
            self.children = []

    def __str__(self):
        return "%s" % (self.node)

    def __repr__(self):
        return "%s" % (self.node)

    def __getitem__(self, key):
        if isinstance(key, int) or isinstance(key, slice):
            return self.children[key]
        if isinstance(key, str):
            for child in self.children:
                if child.node == key: return child

    def __iter__(self):
        return self.children.__iter__()

    def __len__(self):
        return len(self.children)

    @staticmethod
    def get_tree():
        return Tree("t",
                    Tree("rr",
                         Tree("rr1",
                              Tree("yy",
                                   Tree("ab"), Tree("bc")),
                              Tree("zz",
                                   Tree("a"),
                                   Tree("b",
                                        Tree("c"),
                                        Tree("d",
                                             Tree("e"),
                                             Tree("f",
                                                  Tree("g"),
                                                  Tree("h",
                                                       Tree("i"))))))),
                         Tree("rr2", Tree("rr22"))),
                    Tree("root",
                         Tree("l1",
                              Tree("ll1"),
                              Tree("lr1",
                                   Tree("lrl"),
                                   Tree("lrr"))),
                         Tree("r1",
                              Tree("rr2",
                                   Tree("rr3",
                                        Tree("rrl",
                                             Tree("rrll",
                                                  Tree("rrlll",
                                                       Tree("98"), Tree("99")),
                                                  Tree("rrllr")),
                                             Tree("rrlr")))))))


def gentree(path):
    root = Tree(os.path.basename(path))
    if os.path.isdir(path):
        for f in os.listdir(path):
            root.children.append(gentree(os.path.join(path, f)))
    return root
