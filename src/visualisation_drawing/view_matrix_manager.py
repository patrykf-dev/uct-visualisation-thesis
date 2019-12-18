import numpy as np

from src.utils.math_utils import expotential_function, normalize


class ViewMatrixManager:
    SMOOTH_TRANSLATION_MODIFIER = 2
    MAX_ZOOM_IN_TICS = 75
    MAX_ZOOM_OUT_TICS = -20

    def __init__(self):
        self.x_from_center = 0
        self.y_from_center = 0
        self.scale = 0.9
        self._scale_tics = 0
        self.view_matrix_1 = np.eye(4, dtype=np.float32)
        self.view_matrix_2 = np.eye(4, dtype=np.float32)
        self.projection_matrix_1 = np.eye(4, dtype=np.float32)
        self.projection_matrix_2 = np.eye(4, dtype=np.float32)
        self._update_matrix()

    def zoom_out(self):
        if self._scale_tics > self.MAX_ZOOM_OUT_TICS:
            self._scale_tics -= 1
            self._update_scale()
            self._update_matrix()

    def zoom_in(self):
        if self._scale_tics < self.MAX_ZOOM_IN_TICS:
            self._scale_tics += 1
            self._update_scale()
            self._update_matrix()

    def translate_view(self, x_diff, y_diff):
        x_diff_scaled = ViewMatrixManager.SMOOTH_TRANSLATION_MODIFIER * (x_diff / self.scale)
        y_diff_scaled = ViewMatrixManager.SMOOTH_TRANSLATION_MODIFIER * (y_diff / self.scale)
        self.x_from_center += x_diff_scaled
        self.y_from_center += y_diff_scaled
        self._update_matrix()

    def reset_view(self):
        self.x_from_center = 0
        self.y_from_center = 0
        self.scale = 0.9
        self._scale_tics = 0
        self._update_matrix()

    def _update_scale(self):
        a = 0.9
        b = 1.099996548
        self.scale = expotential_function(self._scale_tics, a, b)

    def _update_matrix(self):
        self._apply_translation()
        self._apply_scale()

    def _apply_translation(self):
        view = self._look_at(self.x_from_center, self.y_from_center)
        self.view_matrix_1 = view
        self.view_matrix_2 = view

    def _apply_scale(self):
        projection = self._perspective()
        self.projection_matrix_1 = projection
        self.projection_matrix_2 = projection

    def _perspective(self):
        left = -1 / self.scale + self.x_from_center
        right = 1 / self.scale + self.x_from_center
        bottom = -1 / self.scale + self.y_from_center
        top = 1 / self.scale + self.y_from_center
        rc = np.array([
            [2 / (right - left), 0, 0, 0],
            [0, 2 / (top - bottom), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
        return rc

    def _look_at(self, x, y):
        eye = np.array([x, y, 0])
        center = np.array([x, y, 1])
        up = np.array([0, -1, 0])
        z = normalize(eye - center)
        x = normalize(np.cross(up, z))
        y = normalize(np.cross(z, x))
        rc = np.array([
            [x[0], x[1], x[2], np.dot(-x, eye)],
            [y[0], -y[1], y[2], np.dot(-y, eye)],
            [z[0], z[1], z[2], np.dot(-z, eye)],
            [0, 0, 0, 1]]).transpose()
        return rc

    def parse_click(self, x_clicked, y_clicked, width, height):
        seen_world_up = (-1 / self.scale) + self.y_from_center
        seen_world_down = (1 / self.scale) + self.y_from_center
        seen_world_right = (1 / self.scale) + self.x_from_center
        seen_world_left = (-1 / self.scale) + self.x_from_center
        world_x_span = seen_world_right - seen_world_left
        world_y_span = seen_world_down - seen_world_up
        fract_clicked_x = x_clicked / width
        fract_clicked_y = y_clicked / height
        world_x = fract_clicked_x * world_x_span + seen_world_left
        world_y = - (fract_clicked_y * world_y_span + seen_world_up)
        return world_x, world_y
