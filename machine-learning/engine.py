import chess
import numpy as np
from pystockfish import *

class ChessEngine(object):
    def __init__(self, depth = 1):
        self.depth = depth
    
    def makeMove(self, board, moveFunction=None):
        move = self. alphabeta(
            board, self.depth, float('-infinity'), float('+infinity')
        )[1]
        if moveFunction is not None:
            moveFunction(move)
        else:
            return move

    def alphabeta(self, board, depth, alpha, beta):
        if board.is_game_over():
            result = board.result()
            if result == "1-0":
                return 1, None
            elif result == "0-1":
                return -1, None
            elif result == "1/2-1/2":
                return 0, None
            else:
                print("Unknown board result!")
                return 0, None

        if depth == 0: return self.evaluate(board), None

        # If it is whites turn
        if board.turn:
            bestmove = None
            for move in board.legal_moves:
                board.push(move)
                score, submove = self.alphabeta(board, depth - 1, alpha, beta)
                board.pop()

                if score > alpha:
                    alpha = score
                    bestmove = move
                    if alpha >= beta:
                        break
            return alpha, bestmove
        else:
            bestmove = None
            for move in board.legal_moves:
                board.push(move)
                score, submove = self.alphabeta(board, depth - 1, alpha, beta)
                board.pop()

                if score < beta:
                    beta = score
                    bestmove = move
                    if alpha >= beta:
                        break
            return beta, bestmove

    def evaluate(self, board):
        return 0

class SimpleStockFish(ChessEngine):
    def __init__(self, depth = 15):
        self.engine = Engine(depth=depth)
        ChessEngine.__init__(self, depth)

    def makeMove(self, board, moveFunction=None):
        self.engine.setfenposition(board.fen())
        move = self.engine.bestmove()["move"]
        if moveFunction is not None:
            moveFunction(chess.Move.from_uci(move))
        else:
            return move

    def evaluate(self, board):
        self.engine.setfenposition(board.fen())
        info = self.engine.bestmove()["info"]
        endOfScoreIndex = info.find(" nodes")
        endOfScoreIndex = len(info) if endOfScoreIndex == -1 else endOfScoreIndex

        # If the score is in centipawns, get it and transform it to -1 to 1
        if "score cp" in info:
            centipawns = info[info.find("score cp ") + len("score cp "): endOfScoreIndex]
            return np.tanh(int(centipawns) / 833.3) * (int(board.turn) * 2 - 1)

        # If the score is in moves to mate, return the value of the winning side
        elif "score mate" in info:
            mate = info[info.find("score mate ") + len("score mate "): endOfScoreIndex]
            return 1 if int(mate) > 0 else -1

        # Otherwise, there is some format I didn't account for!
        else:
            print("BIG PROBLEM!  We can't find the stockfish score")