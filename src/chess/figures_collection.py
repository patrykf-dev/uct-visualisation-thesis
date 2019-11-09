import src.utils.array_utils as ArrayUtils
from src.chess.enums import FigureType, Color


class ChessFiguresCollection:
    def __init__(self, figures):
        self._figures_array = ArrayUtils.generate_2d_nones_array(8, 8)
        self.figures_list = []
        self.player1_value = 0
        self.player2_value = 0
        for figure in figures:
            self.add_figure(figure)

    def decrease_collection_value(self, figure):
        if figure.color == Color.WHITE:
            self.player1_value -= figure.value
        else:
            self.player2_value -= figure.value

    def increase_collection_value(self, figure):
        if figure.color == Color.WHITE:
            self.player1_value += figure.value
        else:
            self.player2_value += figure.value

    def remove(self, figure):
        self.decrease_collection_value(figure)
        self.figures_list.remove(figure)
        self._set_figure_in_array(figure.position, None)

    def remove_figure_at(self, position):
        self.remove(self._get_figure_from_array(position))

    def get_figure_at(self, position):
        return self._get_figure_from_array(position)

    def add_figure(self, figure):
        self.increase_collection_value(figure)
        self.figures_list.append(figure)
        self._set_figure_in_array(figure.position, figure)

    def get_king_position(self, color):
        # TODO: optimize
        for fig in self.figures_list:
            if fig.figure_type == FigureType.KING and fig.color == color:
                return fig.position
        return None

    def move_figure_at(self, old_position, new_position):
        figure = self._get_figure_from_array(old_position)
        self.move_figure_to(figure, new_position)

    def move_figure_to(self, figure, new_position):
        self._set_figure_in_array(new_position, figure)
        self._set_figure_in_array(figure.position, None)
        figure.position = new_position

    def restore(self, figure, previous_position):
        figure.position = previous_position
        self._set_figure_in_array(figure.position, figure)

    def temporarily_disable(self, figure):
        self._set_figure_in_array(figure.position, None)
        figure.position = (999, 999)

    def _get_figure_from_array(self, position):
        x = position[0]
        y = position[1]
        return self._figures_array[x][y]

    def _set_figure_in_array(self, position, figure):
        x = position[0]
        y = position[1]
        self._figures_array[x][y] = figure
