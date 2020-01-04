import src.chess.chess_utils as ChessUtils
from src.chess.board_gui import BoardGUI
from src.chess.chess_canvas_drawer import ChessCanvasDrawer
from src.chess.chessboard import Chessboard
from src.chess.enums import TileMarkType
from src.chess.figures import Figure


class ChessGameManager:
    """
    This class has information about board logic and its GUI. It handles clicks on a tile: selects/deselects figure.
    """
    def __init__(self, width, height):
        self.board = Chessboard()
        self.if_figure_selected = False
        self.selected_tile = None
        self.canvas_drawer = ChessCanvasDrawer(width, height, self)
        self.board_gui = BoardGUI(self.canvas_drawer.tiles_count, self.canvas_drawer.tile_width,
                                  self.canvas_drawer.tile_height)
        self.board.notify_tile_marked += self.on_tile_marked

    def on_tile_marked(self, sender, args):
        """
        Marks the appropriate tile after check is detected always after the move, to mark moved piece.
        :param sender: information about object that sends the notification
        :param args: handler additional arguments, in this case TileMarkArgs object
        :return: None
        """
        if args.tile_mark_type == TileMarkType.CHECKED:
            self.board_gui.mark_tile_checked(args.pos)
        elif args.tile_mark_type == TileMarkType.MOVED:
            self.board_gui.mark_tile_moved(args.pos)

    def react_to_tile_click(self, grid_pos):
        """
        Reacts when user clicks at chess GUI:
        Selects the clicked figure or deselects it. When figure was already chosen and a possible move was clicked,
        the move is executed.
        :param grid_pos: tuple indicating a tile
        :return: tuple of 2 values: bool if a move was made, a move itself (ChessMove object)
        """
        if not self.if_figure_selected:
            self.select_figure(grid_pos)
            return False, None
        else:
            positions_list = [x.position_to for x in self.board.possible_moves]
            move_index = positions_list.index(grid_pos) if grid_pos in positions_list else -1
            if move_index != -1:
                move = self.board.possible_moves[move_index]
                self.deselect_last_moved()
                self.deselect_king()
                self.board.perform_legal_move(move)
                self.reset_selected_tile()
                return True, move
            else:
                if self.selected_tile:
                    self.deselect_figure()
                self.select_figure(grid_pos)
                return False, None

    def select_figure(self, grid_pos):
        """
        Selects figure and remembers the possible moves of it. It selects only, when a tile with figure was chosen and
        its color matches the current moving player. Otherwise, the currently selected figure is deselected.
        :param grid_pos: tuple indicating a tile
        :return: None
        """
        figure = Figure.get_figure(self.board.figures, grid_pos)
        if figure and figure.color == self.board.current_player_color:
            self.board_gui.mark_tile_selected(grid_pos)
            self.if_figure_selected = True
            self.selected_tile = grid_pos
            available_moves = figure.check_moves(self.board.figures)
            ChessUtils.reduce_move_range_when_check(self.board, figure, available_moves)
            self.board.possible_moves = available_moves
        else:
            self.deselect_figure()

    def deselect_last_moved(self):
        """
        Deselects move that was marked as executed previously.
        :return: None
        """
        if not self.board.past_moves:
            return
        tile_1 = self.board.past_moves[-1].position_to
        tile_2 = self.board.past_moves[-1].position_from
        self.board_gui.mark_tile_deselected(tile_1)
        self.board_gui.mark_tile_deselected(tile_2)

    def deselect_figure(self):
        """
        Deselects figure - make its tile unmarked. If it was king that got checked, the check mark is kept.
        :return: None
        """
        if self.selected_tile:
            is_king_selected = ChessUtils.is_king_selected_to_move_in_check(self.board, self.selected_tile)
            self.board_gui.mark_tile_deselected(self.selected_tile, when_checked=is_king_selected)
        self.reset_selected_tile()

    def reset_selected_tile(self):
        """
        After deselecting figure this function clears the possible moves list.
        :return: None
        """
        self.selected_tile = None
        self.board.possible_moves = []
        self.if_figure_selected = False

    def deselect_king(self):
        """
        Deselects king after running away from check.
        :return: None
        """
        if self.board.check:
            self.board_gui.mark_tile_deselected(self.board.figures.get_king_position(self.board.current_player_color))
