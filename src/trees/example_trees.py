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
    prev = aa
    for i in range(5):
        new_node = create_node("xx", "z")
        prev.add_child_by_node(new_node)
        for i in range(3):
            prev.add_child_by_node(create_node("asd", "asd"))
        prev = new_node
    return aa
