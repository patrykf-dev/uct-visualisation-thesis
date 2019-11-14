import numpy as np


class ViewMatrixManager:
    def __init__(self):
        self.x_from_center = 0
        self.y_from_center = 0
        self.scale = 0.9
        self.view_matrix_1 = np.eye(4, dtype=np.float32)
        self.view_matrix_2 = np.eye(4, dtype=np.float32)
        self.projection_matrix_1 = np.eye(4, dtype=np.float32)
        self.projection_matrix_2 = np.eye(4, dtype=np.float32)
        self._update_matrix()

    def change_scale(self, scale):
        self.scale = scale
        self._update_matrix()

    def translate_view(self, x_diff, y_diff):
        self.x_from_center += x_diff
        self.y_from_center += y_diff
        self._update_matrix()

    def reset_view(self):
        self.x_from_center = 0
        self.y_from_center = 0
        self.scale = 0.9
        self._update_matrix()

    def _update_matrix(self):
        self._apply_translation()
        self._apply_scale()

    def _apply_translation(self):
        view = self.look_at(self.x_from_center, self.y_from_center)
        for i in range(4):
            for j in range(4):
                self.view_matrix_1[i][j] = view[i][j]
                self.view_matrix_2[i][j] = view[i][j]

    def _apply_scale(self):
        projection = self.perspective()
        self.projection_matrix_1 = projection
        self.projection_matrix_2 = projection

    def perspective(self):
        left = -1 / self.scale + self.x_from_center
        right = 1 / self.scale + self.x_from_center
        bottom = -1 / self.scale + self.y_from_center
        top = 1 / self.scale + self.y_from_center
        rc = np.array([
            [2 / (right - left), 0, 0, 0],
            [0, 2 / (top - bottom), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        return rc

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

    def parse_click(self, x_clicked, y_clicked, width, height):
        seen_world_up = (-1 / self.scale) + self.y_from_center
        seen_world_down = (1 / self.scale) + self.y_from_center
        seen_world_right = (1 / self.scale) + self.x_from_center
        seen_world_left = (1 / -self.scale) + self.x_from_center

        print(f"{seen_world_up}, {seen_world_down} [][] {seen_world_left}, {seen_world_right}")

        world_x_span = seen_world_right - seen_world_left
        world_y_span = seen_world_down - seen_world_up

        fract_clicked_x = x_clicked / width
        fract_clicked_y = y_clicked / height

        world_x = fract_clicked_x * world_x_span + seen_world_left
        world_y = - (fract_clicked_y * world_y_span + seen_world_up)

        print(f"WORLD SPACE: {world_x}, {world_y}")

        return world_x, world_y
