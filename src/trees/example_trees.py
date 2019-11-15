import random

from src.uct.algorithm.mc_node import MonteCarloNode


def create_node(name, move_name):
    n = MonteCarloNode()
    n.details.state_name = name
    if len(move_name) > 0:
        n.details.move = move_name
        n.details.visits_count = 3
        n.details.visits_count_pre_modified = 4
        n.details.average_prize = 4.5
    return n


def create_canvas_tree():
    a = create_node("aa", "")
    b = create_node("bb", "x")
    c = create_node("cc", "y")
    d = create_node("dd", "z")
    e = create_node("ee", "w")
    a.add_child_by_node(b)
    b.add_child_by_node(c)
    c.add_child_by_node(d)
    d.add_child_by_node(e)
    a.vis_details.x = 1
    a.vis_details.y = 1
    b.vis_details.x = -1
    b.vis_details.y = 1
    c.vis_details.x = -1
    c.vis_details.y = -1
    d.vis_details.x = 1
    d.vis_details.y = -1
    e.vis_details.x = 0
    e.vis_details.y = 0
    return a


def create_sample_tree_1():
    """
    Small binary tree
    :return: root of the tree
    """
    root = create_node("root", "asd")
    left = create_node("left", "asd")
    right = create_node("right", "asd")
    root.add_child_by_node(left)
    root.add_child_by_node(right)
    left.add_child_by_node(create_node("123", "123"))
    left.add_child_by_node(create_node("123", "123"))
    right.add_child_by_node(create_node("123", "123"))
    right.add_child_by_node(create_node("123", "123"))
    return root


def create_sample_tree_2():
    """
    Small full ternary tree
    :return: root of the tree
    """
    root = create_node("root", "asd")
    prevs = [root]
    for i in range(3):
        new_prevs = []
        for node in prevs:
            for j in range(3):
                new_child = create_node(f"{i}, {j}", "asd")
                node.add_child_by_node(new_child)
                new_prevs.append(new_child)
        prevs = new_prevs
    return root


def create_sample_tree_3():
    """
    Small non full ternary tree
    :return: root of the tree
    """
    root = create_node("root", "asd")
    prevs = [root]
    for i in range(4):
        new_prevs = []
        for node in prevs:
            for j in range(3):
                guess = random.randint(0, 10)
                if guess > 7:
                    continue
                new_child = create_node(f"{i}, {j}", "asd")
                node.add_child_by_node(new_child)
                new_prevs.append(new_child)
        prevs = new_prevs
    return root


def create_sample_tree_4():
    """
    Left-grown tree (most of parent vertices are on the left)
    :return: root of the tree
    """
    root = create_node("root", "asd")
    parent_vertex = root
    for i in range(7):
        child_count = random.randint(8, 12)
        for j in range(child_count):
            new_child = create_node(f"{i}, {j}", "asd")
            parent_vertex.add_child_by_node(new_child)
        parent_index = random.randint(0, 3)
        parent_vertex = parent_vertex.children[parent_index]
    return root


def create_sample_tree_5():
    """
    Weird tree, described below
    :return: root of the tree
    """
    aa = create_node("aa", "")
    bb = create_node("bb", "x")
    cc = create_node("cc", "y")
    dd = create_node("dd", "z")
    ee = create_node("ee", "w")
    ff = create_node("ee", "w")
    gg = create_node("ee", "w")
    hh = create_node("ee", "w")

    aa.add_child_by_node(bb)
    aa.add_child_by_node(create_node("asd", "asd"))
    aa.add_child_by_node(gg)
    aa.add_child_by_node(cc)
    cc.add_child_by_node(dd)
    dd.add_child_by_node(hh)
    cc.add_child_by_node(ee)
    cc.add_child_by_node(ff)
    prev1 = aa
    prev2 = dd
    prev3 = gg
    for i in range(10):
        new_node = create_node("xx", "z")
        new_node2 = create_node("xx", "z")
        prev1.add_child_by_node(new_node)
        prev2.add_child_by_node(new_node2)
        child_count1 = i % 4
        child = create_node("asd", "asd")
        prev3.add_child_by_node(child)
        for j in range(child_count1):
            prev1.add_child_by_node(create_node("asd", "asd"))
        child_count2 = i % 3
        for j in range(child_count2):
            prev2.add_child_by_node(create_node("asd", "asd"))
        prev1 = new_node
        prev2 = new_node2
        prev3 = child
    return aa


def create_sample_tree_6():
    """
    A rather broad tree, but more random than 8
    :return: root of the tree
    """
    root = create_node("root", "asd")
    prevs = [root]
    for i in range(4):
        new_prevs = []
        for node in prevs:
            child_count = random.randint(2, 7)
            for j in range(child_count):
                new_child = create_node(f"{i}, {j}", "asd")
                node.add_child_by_node(new_child)
                new_prevs.append(new_child)

        prevs = new_prevs

    return root


def create_sample_tree_7():
    """
    Totally random tree
    :return: root of the tree
    """
    root = create_node("root", "asd")
    addable = [root]
    for i in range(500):
        new_node = create_node(f"vertex {i}", "asd")
        parent_index = random.randint(0, len(addable) - 1)
        addable[parent_index].add_child_by_node(new_node)
        addable.append(new_node)

    return root


def create_sample_tree_8():
    """
    Creates broad tree - every non-leaf vertrex contains a lot of children
    :return: root of the tree
    """
    root = create_node("root", "asd")
    addable = [root]
    for i in range(100):
        parent_index = random.randint(0, len(addable) - 1)
        prev = addable[parent_index]
        for j in range(10):
            new_node = create_node(f"{i} {j} coordinates", "asd")
            prev.add_child_by_node(new_node)
        addable.append(new_node)
    return root


def create_sample_tree_09():
    """
    Creates kind of "chain" tree - a lot of narrow paths
    :return: root of the tree
    """
    root = create_node("root", "asd")
    addable = [root]
    for i in range(20):
        parent_index = random.randint(0, len(addable) - 1)
        prev = addable[parent_index]
        for j in range(20):
            new_node = create_node(f"{i} {j} coordinates", "asd")
            prev.add_child_by_node(new_node)
            prev = new_node
        addable.append(new_node)
    return root


def create_sample_tree_10():
    """
    Most UCT-like tree
    :return: root of the tree
    """
    root = create_node("root", "asd")
    prevs = [root]
    for i in range(5):
        new_prevs = []
        for node in prevs:
            child_count = random.randint(3, 8)
            guess = random.randint(0, 10)
            if guess > 5:
                continue
            for j in range(child_count):
                new_child = create_node(f"{i}, {j}", "asd")
                node.add_child_by_node(new_child)
                new_prevs.append(new_child)

        prevs = new_prevs
    return root
