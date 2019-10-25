import chess
import sys
from neural_network import *
from state import State
from engine import *

class NeuralEngine(ChessEngine):
    def __init__(self, depth=1, checkpoints=None):
        super().__init__(depth=depth)
        self.model = Model(checkpoints)
    
    def evaluate(self, board):
        s = State(board)
        return self.model.runInput(s.getBoardFeature())


if __name__ == "__main__":
    modelSave = sys.argv[1]
    argChessString = sys.argv[2]
    board = chess.Board(argChessString)

    board = chess.Board()
    AI = NeuralEngine(depth=3, checkpoints=modelSave)
    print(AI.makeMove(board))