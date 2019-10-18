import chess.pgn
import os

values = {'1/2-1/2':0, '0-1':-1, '1-0':1}

def board_print(board):
    os.system('clear')
    print(board)

def get_dataset(pgn):
    while 1:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        res = game.headers['Result']
        if res not in values:
            continue
        value = values[res]
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            # board_print(board)


def load_data():
    for fn in os.listdir("data"):
        pgn = open(os.path.join("data"), fn)
        get_dataset(pgn)

if __name__ == "__main__":
    pgn = open(os.path.join("data/KingBase2019-A00-A39.pgn"))
    get_dataset(pgn)