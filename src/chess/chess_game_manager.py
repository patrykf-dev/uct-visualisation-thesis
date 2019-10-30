import src.chess.chess_utils as ChessUtils
from src.chess.board_gui import BoardGUI, TileMarkType
from src.chess.chessboard import Chessboard
from src.chess.figures import Figure


class ChessGameManager:
    def __init__(self):
        self.board = Chessboard()
        self.if_figure_selected = False
        self.selected_tile = None
        self.board_gui = BoardGUI()
        self.board.on_tile_marked += self.on_tile_marked

    def on_tile_marked(self, sender, pos, tile_mark_type):
        if tile_mark_type == TileMarkType.CHECKED:
            self.board_gui.mark_tile_checked(pos)
        elif tile_mark_type == TileMarkType.MOVED:
            self.board_gui.mark_tile_moved(pos)

    def react_to_tile_click(self, grid_pos):
        if not self.if_figure_selected:
            self.select_figure(grid_pos)
            return False
        else:
            positions_list = [x.position_to for x in self.board.possible_moves]
            move_index = positions_list.index(grid_pos) if grid_pos in positions_list else -1
            clicked_possible_move = move_index != -1
            if clicked_possible_move:
                self.deselect_last_moved()
                self.board.perform_legal_move(self.board.possible_moves[move_index], self.selected_tile)
                self.reset_selected_tile()
                return True
            else:
                if self.selected_tile:
                    self.deselect_figure()
                self.select_figure(grid_pos)
                return False

    def select_figure(self, grid_pos):
        figure = Figure.get_figure(self.board.figures, grid_pos)
        if figure and figure.color == self.board.current_player:
            self.board_gui.mark_tile_selected(grid_pos)
            self.if_figure_selected = True
            self.selected_tile = grid_pos
            available_moves = figure.check_moves(self.board.figures)
            self.board.possible_moves = ChessUtils.reduce_move_range_when_check(self.board, figure, available_moves)
        else:
            self.deselect_figure()

    def deselect_last_moved(self):
        if not self.board.past_moves:
            return
        tile_1 = self.board.past_moves[-1].position
        tile_2 = self.board.past_moves[-1].old_position
        self.board_gui.mark_tile_deselected(tile_1)
        self.board_gui.mark_tile_deselected(tile_2)

    def deselect_figure(self):
        if self.selected_tile:
            if not self.board.check:
                self.board_gui.mark_tile_deselected(ChessUtils.get_king_position(self.board, self.board.current_player))
            is_king_selected = ChessUtils.is_king_selected_to_move_in_check(self.board, self.selected_tile)
            self.board_gui.mark_tile_deselected(self.selected_tile, when_checked=is_king_selected)
        self.reset_selected_tile()

    def reset_selected_tile(self):
        self.selected_tile = None
        self.board.possible_moves = []
        self.if_figure_selected = False
