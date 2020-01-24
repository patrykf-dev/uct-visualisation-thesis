from os import path

from main_application.resources_container import ResourcesContainer


class ShaderReader:
    def __init__(self):
        self.shaders_path = ResourcesContainer.inst.base_path
        self.vertives_vshader = self._get_shader("vertex_shader_vertices")
        self.vertives_fshader = self._get_shader("fragment_shader_vertices")
        self.edges_vshader = self._get_shader("vertex_shader_edges")
        self.edges_fshader = self._get_shader("fragment_shader_edges")

    def _get_shader(self, name):
        with open(path.join(self.shaders_path, name + ".c")) as f:
            content = f.read()
        return content
