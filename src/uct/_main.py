from src.tictactoe.game_data import TicTacToeGameData, TicTacToeBoard
import src.uct.enums as Enums


def main():
    game_data = TicTacToeGameData(TicTacToeBoard(3))
    while True:
        x, y = read_player_decision(game_data)
        game_data.board.perform_move(game_data.current_player, x, y)
        print(game_data.board.get_string_formatted())
        game_data.switch_current_player()
        if game_data.board.check_status() != Enums.GamePhase.IN_PROGRESS:
            print("Game end... {}".format(game_data.board.check_status()))
            break


def read_player_decision(game_data):
    while True:
        print("\n")
        x = int(input("Enter player {} x: ".format(game_data.current_player)))
        y = int(input("Enter player {} y: ".format(game_data.current_player)))
        if game_data.board.move_valid(x, y):
            return x, y
        print("Invalid move! Try again please")


main()
