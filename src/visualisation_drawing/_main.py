import numpy as np
import vispy
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from vispy import app as VispyApp
from vispy.gloo import set_viewport, set_state, clear

import src.trees.example_trees as ExampleTrees
from src.uct.algorithm.mc_node import MonteCarloNode
from src.visualisation_algorithm.walkers_algorithm import ImprovedWalkersAlgorithm

vs_vertices = """
#version 410

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform float u_antialias;
uniform float u_size;

attribute vec3  a_position;
attribute vec4  a_fg_color;
attribute vec4  a_bg_color;
attribute float a_linewidth;
attribute float a_size;

varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

void main (void) {
    v_size = a_size * u_size;
    v_linewidth = a_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = a_fg_color;
    v_bg_color  = a_bg_color;
    gl_Position = u_projection * u_view * u_model *
        vec4(a_position*u_size,1.0);
    gl_PointSize = v_size + 2*(v_linewidth + 1.5*v_antialias);
}
"""

fs_vertices = """
#version 410

varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_size;
varying float v_linewidth;
varying float v_antialias;

float marker(vec2 P, float size);

void main()
{
    float size = v_size +2*(v_linewidth + 1.5*v_antialias);
    float t = v_linewidth/2.0-v_antialias;

    // The marker function needs to be linked with this shader
    float r = marker(gl_PointCoord, size);

    float d = abs(r) - t;
    if( r > (v_linewidth/2.0+v_antialias))
    {
        discard;
    }
    else if( d < 0.0 )
    {
       gl_FragColor = v_fg_color;
    }
    else
    {
        float alpha = d/v_antialias;
        alpha = exp(-alpha*alpha);
        if (r > 0)
            gl_FragColor = vec4(v_fg_color.rgb, alpha*v_fg_color.a);
        else
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
    }
}

float marker(vec2 P, float size)
{
    float r = length((P.xy - vec2(0.5,0.5))*size);
    r -= v_size/2;
    return r;
}
"""

vs_edges = """
attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

void main(){
    gl_Position = vec4(a_position, 1.);
}
"""

fs_edges = """
void main(){
    gl_FragColor = vec4(0.2, 0.2, 0.2, 1.0);
}
"""

vertices_count = 0
edges_count = 0


def add_node_data(node: MonteCarloNode, vertices, edges):
    global vertices_count, edges_count
    x = node.vis_details.x / 12
    y = 0.5 - node.vis_details.y / 5.5
    vertices['a_position'][vertices_count] = (x, y, 0)
    parent_counter = vertices_count
    for child in node.children:
        vertices_count = vertices_count + 1
        edges[edges_count] = (vertices_count, parent_counter)
        edges_count = edges_count + 1
        add_node_data(child, vertices, edges)


def generate_graph_data(node: MonteCarloNode, ps):
    global vertices_count
    edges = np.zeros((29, 2)).astype(np.uint32)

    vertices = np.zeros(29, dtype=[('a_position', np.float32, 3),
                                   ('a_fg_color', np.float32, 4),
                                   ('a_bg_color', np.float32, 4),
                                   ('a_size', np.float32),
                                   ('a_linewidth', np.float32)])

    add_node_data(node, vertices, edges)

    vertices_count = vertices_count + 1

    vertices['a_fg_color'] = 0, 0, 0, 1
    color = np.random.uniform(0.1, 1.0, (vertices_count, 3))
    vertices['a_bg_color'] = np.hstack((color, np.ones((vertices_count, 1))))
    vertices['a_size'] = np.random.randint(size=vertices_count, low=15 * ps, high=18 * ps)
    vertices['a_linewidth'] = 1.0 * ps
    return vertices, edges


class MonteCarloTreeCanvas(VispyApp.Canvas):
    def __init__(self, tree, **kwargs):
        VispyApp.Canvas.__init__(self, size=(1000, 1000), **kwargs)
        self.position = 50, 50

        ps = self.pixel_scale
        vertices, edges = generate_graph_data(tree, ps)

        u_antialias = 1

        self.vbo = vispy.gloo.VertexBuffer(vertices)
        self.index = vispy.gloo.IndexBuffer(edges)

        set_viewport(0, 0, *self.physical_size)

        self.program_vertices = vispy.gloo.Program(vs_vertices, fs_vertices)
        self.program_vertices.bind(self.vbo)
        self.program_vertices['u_size'] = 1
        self.program_vertices['u_antialias'] = u_antialias
        self.program_vertices['u_model'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_view'] = np.eye(4, dtype=np.float32)
        self.program_vertices['u_projection'] = np.eye(4, dtype=np.float32)

        self.program_edges = vispy.gloo.Program(vs_edges, fs_edges)
        self.program_edges.bind(self.vbo)

        set_state(clear_color='gray', depth_test=False, blend=True, blend_func=('src_alpha', 'one_minus_src_alpha'))

    def on_resize(self, event):
        set_viewport(0, 0, *event.physical_size)

    def on_draw(self, event):
        clear(color=True, depth=True)
        self.program_edges.draw('lines', self.index)
        self.program_vertices.draw('points')


if __name__ == '__main__':
    root = ExampleTrees.create_tree_1()
    alg = ImprovedWalkersAlgorithm()
    alg.buchheim_algorithm(root)

    canvas = MonteCarloTreeCanvas(root, title="Graph")
    window = QMainWindow()
    widget = QWidget()
    window.setCentralWidget(widget)
    widget.setLayout(QVBoxLayout())
    widget.layout().addWidget(canvas.native)
    widget.layout().addWidget(QPushButton())
    window.show()
    VispyApp.run()
