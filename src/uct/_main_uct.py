import src.uct.enums as Enums
from src.tictactoe.ttt_state import TicTacToeState
from src.tictactoe.board import TicTacToeBoard
from src.uct.mc_tree_search import MonteCarloTreeSearch


def player_vs_player():
    game_data = TicTacToeState(TicTacToeBoard(3))
    while True:
        x, y = read_player_decision(game_data)
        game_data.board.perform_move(game_data.current_player, x, y)
        print(game_data.board.get_string_formatted())
        game_data.switch_current_player()
        if game_data.board.check_status() != Enums.GamePhase.IN_PROGRESS:
            print("Game end... {}".format(game_data.board.check_status()))
            break


def player_vs_machine():
    game_data = TicTacToeState(TicTacToeBoard(3))
    while True:
        x, y = read_player_decision(game_data)
        game_data.board.perform_move(game_data.current_player, x, y)

        mcts = MonteCarloTreeSearch()
        game_data = mcts.find_next_move(game_data)

        print(game_data.board.get_string_formatted())
        game_data.switch_current_player()

        if game_data.board.check_status() != Enums.GamePhase.IN_PROGRESS:
            print("Game end... {}".format(game_data.board.check_status()))
            break

def machine_vs_machine():
    game_state = TicTacToeGameData(TicTacToeBoard(7))
    while True:
        mcts = MonteCarloTreeSearch()
        next_game_state = mcts.find_next_move(game_state)

        game_state = next_game_state
        print("\nCurrent player: {}".format(game_state.current_player))
        print(game_state.board.get_string_formatted())

        if game_state.board.check_status() != Enums.GamePhase.IN_PROGRESS:
            print("Game end... {}".format(game_state.board.check_status()))
            break

def read_player_decision(game_data):
    while True:
        print("\n")
        x = int(input("Enter player {} x: ".format(game_data.current_player)))
        y = int(input("Enter player {} y: ".format(game_data.current_player)))
        if game_data.board.move_valid(x, y):
            return x, y
        print("Invalid move! Try again please")


# CALL MAIN METHOD
machine_vs_machine()
