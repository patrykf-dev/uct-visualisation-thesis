
import utils.array_utils as ArrayUtils
from chess.enums import FigureType, Color


class ChessFiguresCollection:
    """
    Class contains information about figures list and values of each team's figure collection.
    It uses a few optimizations:
    - getting and setting figures involves using two-dimensional numpy array
    - kings' positions are cached.
    """
    FIGURES_MAX_VALUE = 39

    def __init__(self, figures):
        self._figures_array = ArrayUtils.generate_2d_nones_array(8, 8)
        self.figures_list = []
        self.player1_value = 0
        self.player2_value = 0
        self.white_king = None
        self.black_king = None
        for figure in figures:
            self.add_figure(figure)

    def get_king(self, color):
        """
		Args:
			color:  Color enum object

		Returns:
			king of given color        
		"""
        return self.white_king if color == Color.WHITE else self.black_king

    def get_king_position(self, color):
        """
		Args:
			color:  Color enum object

		Returns:
			king's position of given color        
		"""
        return self.get_king(color).position

    def decrease_collection_value(self, figure):
        """
        Decreases value of one collection (white or black), depending on given figure's color by its value.

		Args:
			figure:  Figure object

		Returns:
			None        
		"""
        if figure.color == Color.WHITE:
            self.player1_value -= figure.value
        else:
            self.player2_value -= figure.value

    def increase_collection_value(self, figure):
        """
        Increases value of one collection (white or black), depending on given figure's color by its value.

		Args:
			figure:  Figure object

		Returns:
			None        
		"""
        if figure.color == Color.WHITE:
            self.player1_value += figure.value
        else:
            self.player2_value += figure.value

    def set_king_reference(self, figure):
        """
        Caches king in class field, depending on its color.

		Args:
			figure:  Figure object, assuming it's the king

		Returns:
			None        
		"""
        if figure.color == Color.WHITE:
            self.white_king = figure
        else:
            self.black_king = figure

    def remove(self, figure):
        """
        Removes figure from list. It decreases collection value.

		Args:
			figure:  Figure object

		Returns:
			index of where the figure was placed in the list        
		"""
        self.decrease_collection_value(figure)
        index = self.figures_list.index(figure)
        self.figures_list.pop(index)
        self._set_figure_in_array(figure.position, None)
        return index

    def remove_figure_at(self, position):
        """
        Removes figure from list. It decreases collection value.

		Args:
			position:  tuple of figure's position

		Returns:
			None        
		"""
        self.remove(self._get_figure_from_array(position))

    def get_figure_at(self, position):
        """
		Args:
			position:  tuple of figure's position

		Returns:
			figure from array        
		"""
        return self._figures_array[position[0]][position[1]]

    def add_figure(self, figure, figure_index=-1):
        """
        Adds figure to list. It increases collection value.
        Figure is placed at the index given. Otherwise, it is appended to the end.

		Args:
			figure:  Figure object
			figure_index:  index where the figure shall be placed

		Returns:
			None        
		"""
        if figure.figure_type == FigureType.KING:
            self.set_king_reference(figure)
        self.increase_collection_value(figure)
        if figure_index == -1:
            self.figures_list.append(figure)
        else:
            self.figures_list.insert(figure_index, figure)
        self._set_figure_in_array(figure.position, figure)

    def move_figure_at(self, old_position, new_position):
        """
        Changes figure's position by given old position and places it in the new position.

		Args:
			old_position:  tuple
			new_position:  tuple

		Returns:
			None        
		"""
        figure = self._get_figure_from_array(old_position)
        self.move_figure_to(figure, new_position)

    def move_figure_to(self, figure, new_position):
        """
        Changes given figure's position and places it in the new position.

		Args:
			figure:  Figure object
			new_position:  tuple

		Returns:
			None        
		"""
        self._set_figure_in_array(new_position, figure)
        self._set_figure_in_array(figure.position, None)
        figure.position = new_position

    def restore(self, figure, previous_position):
        """
        Restores given figure's position.

		Args:
			figure:  Figure object
			previous_position:  tuple

		Returns:
			None        
		"""
        figure.position = previous_position
        self._set_figure_in_array(figure.position, figure)

    def temporarily_disable(self, figure):
        """
        Fakes removing figure from list.

		Args:
			figure:  Figure object

		Returns:
			None        
		"""
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

