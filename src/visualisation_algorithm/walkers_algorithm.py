from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_algorithm.mc_node_vis_details import MonteCarloNodeVisualisationDetails


def buchheim(root: MonteCarloNode):
    root = firstwalk(root)
    min = second_walk(root)
    if min < 0:
        third_walk(root, -min)
    return root


def firstwalk(node: MonteCarloNode, distance=1):
    if len(node.children) == 0:
        if node.lmost_sibling:
            node.vis_details.x = node.lbrother().vis_details.x + distance
        else:
            node.vis_details.x = 0
    else:
        default_ancestor = node.children[0]
        for w in node.children:
            firstwalk(w)
            default_ancestor = apportion(w, default_ancestor, distance)
        execute_shifts(node)

        midpoint = (node.children[0].vis_details.x + node.children[-1].vis_details.x) / 2

        w = node.lbrother()
        if w:
            node.vis_details.x = w.vis_details.x + distance
            node.vis_details.mod = node.vis_details.x - midpoint
        else:
            node.vis_details.x = midpoint
    return node


def second_walk(node: MonteCarloNode, m=0, depth=0, min=None):
    node.vis_details.x += m
    node.vis_details.y = depth

    if min is None or node.vis_details.x < min:
        min = node.vis_details.x

    for w in node.children:
        min = second_walk(w, m + node.vis_details.mod, depth + 1, min)

    return min


def third_walk(node: MonteCarloNode, n):
    node.vis_details.x += n
    for c in node.children:
        third_walk(c, n)


def apportion(node: MonteCarloNode, default_ancestor, distance):
    left_brother = node.lbrother()
    if left_brother is not None:
        # in buchheim notation:
        # i == inner; o == outer; r == right; l == left; r = +; l = -
        vir = vor = node
        vil = left_brother
        vol = node.lmost_sibling
        sir = sor = node.vis_details.mod
        sil = vil.vis_details.mod
        sol = vol.vis_details.mod
        while vil.right() and vir.left():
            vil = vil.right()
            vir = vir.left()
            vol = vol.left()
            vor = vor.right()
            vor.ancestor = node
            shift = (vil.x + sil) - (vir.x + sir) + distance
            if shift > 0:
                move_subtree(ancestor(vil, node, default_ancestor), node, shift)
                sir = sir + shift
                sor = sor + shift
            sil += vil.mod
            sir += vir.mod
            sol += vol.mod
            sor += vor.mod
        if vil.right() and not vor.right():
            vor.thread = vil.right()
            vor.vis_details.mod += sil - sor
        else:
            if vir.left() and not vol.left():
                vol.thread = vir.left()
                vol.vis_details.mod += sir - sol
            default_ancestor = node
    return default_ancestor


def move_subtree(w_left: MonteCarloNode, w_right: MonteCarloNode, shift):
    subtrees = w_right.number - w_left.number
    w_right.vis_details.change -= shift / subtrees
    w_right.vis_details.shift += shift
    w_left.vis_details.change += shift / subtrees
    w_right.vis_details.x += shift
    w_right.vis_details.mod += shift


def execute_shifts(v: MonteCarloNode):
    shift = change = 0
    for child in v.children[::-1]:
        child.vis_details.x += shift
        child.vis_details.mod += shift
        change += child.vis_details.change
        shift += child.vis_details.shift + change


def ancestor(node: MonteCarloNodeVisualisationDetails, v: MonteCarloNode, default_ancestor):
    # TODO: fix it
    siblings = []
    for sibling in v.parent.children:
        siblings.append(sibling.vis_details)

    if node.ancestor in siblings:
        return node.ancestor
    else:
        return default_ancestor
