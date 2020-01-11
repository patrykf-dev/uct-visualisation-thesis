from os import path


class ShaderReader:
    def __init__(self):
        from main import APP_CONTEXT
        self.shaders_path = APP_CONTEXT.get_resource()

    def get_vertices_vshader(self):
        return self._get_shader("vertex_shader_vertices")

    def get_vertices_fshader(self):
        return self._get_shader("fragment_shader_vertices")

    def get_edges_vshader(self):
        return self._get_shader("vertex_shader_edges")

    def get_edges_fshader(self):
        return self._get_shader("fragment_shader_edges")

    def _get_shader(self, name):
        with open(path.join(self.shaders_path, name + ".c")) as f:
            content = f.read()
        return content
