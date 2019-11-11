import numpy as np


class ViewMatrixManager:
    def __init__(self):
        self.view_matrix_1 = np.eye(4, dtype=np.float32)
        self.view_matrix_2 = np.eye(4, dtype=np.float32)
        self.x = 0
        self.y = 0
        self.scale = 1

    def change_scale(self, scale):
        self.scale = scale
        self._update_matrix()

    def translate_view(self, x_diff, y_diff):
        self.x += x_diff
        self.y += y_diff
        self._update_matrix()

    def _update_matrix(self):
        self._apply_translation()
        self._apply_scale()
        self.view_matrix_1 = np.copy(self.view_matrix_1)
        self.view_matrix_2 = np.copy(self.view_matrix_1)

    def _apply_translation(self):
        view = self.look_at(self.x, self.y)
        for i in range(4):
            for j in range(4):
                self.view_matrix_1[i][j] = view[i][j]
                self.view_matrix_2[i][j] = view[i][j]

    def _apply_scale(self):
        indices = [0, 1, 2]
        for index in indices:
            self.view_matrix_1[index][index] = self.scale
            self.view_matrix_2[index][index] = self.scale

    def look_at(self, x, y):
        eye = np.array([x, y, 0])
        center = np.array([x, y, 1])
        up = np.array([0, -1, 0])
        z = eye - center
        z = self.normalize(z)
        x = np.cross(up, z)
        y = np.cross(z, x)
        x = self.normalize(x)
        y = self.normalize(y)
        rc = np.array([
            [x[0], x[1], x[2], np.dot(-x, eye)],
            [y[0], -y[1], y[2], np.dot(-y, eye)],
            [z[0], z[1], z[2], np.dot(-z, eye)],
            [0, 0, 0, 1]
        ]).transpose()
        return rc

    @staticmethod
    def normalize(v):
        norm = np.linalg.norm(v, ord=1)
        if norm == 0:
            norm = np.finfo(v.dtype).eps
        return v / norm
