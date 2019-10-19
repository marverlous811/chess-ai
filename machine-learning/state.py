import chess
import numpy as np
import random
import itertools
import time

## piece info
pieces = {'r': 2, 'n': 2, 'b': 2, 'q': 1, 'k': 1, 'p': 8}
pieceValues = {'r': 5, 'n': 3, 'b': 3, 'q': 9, 'k': 25, 'p': 1}
rookMovement = [np.array([0, 1]), np.array([1, 0]), np.array([-1, 0]), np.array([0, -1])]
bishopMovement = [np.array([1, 1]), np.array([-1, 1]), np.array([1, -1]), np.array([-1, -1])]
sliding = {'r': rookMovement, 'b': bishopMovement, 'q': rookMovement + bishopMovement}

class State(object):
    def __init__(self, board=None):
        if board is None:
            self.board = chess.Board()
        else:
            self.board = board
        self.boardArray = self.buildBoardArray()

    def key(self):
        return (self.board.board_fen(), self.board.turn, self.board.castling_rights, self.board.ep_square)

    def edges(self):
        return list(self.board.legal_moves)

    ## get the value of the lowest value attacker and defender of the square depending on the color
    ## or the piece color on the sqIndex
    def getLowestAttackerDefender(self, sqIndex, color = None):
        sqUci = chr(sqIndex[1] + ord('a')) + str(8 - sqIndex[0])
        prefix = 'a1' if sqUci != 'a1' else 'a2'
        sqID = chess.Move.from_uci(sqUci + prefix).from_square
        color = color if color is not None else board.piece_at(sqID).color

        lowAtk = 100
        lowDef = 100
        for attSq in self.board.attackers(not color, sqID):
            piece = board.piece_at(attSq)
            lowAtk = min(pieceValues[piece.symbol().lower()], lowAtk)
        for defSq in self.board.attackers(color, sqID):
            piece = board.piece_at(defSq)
            lowDef = min(pieceValues[piece.symbol().lower()], lowDef)

        lowAtk = 0 if lowAtk == 100 else 1.0 / lowAtk
        lowDef = 0 if lowDef == 100 else 1.0 / lowDef
        return lowAtk, lowDef

    def getPieceMobility(self, index, p):
        feature = np.zeros(len(sliding[p.lower()]))
        i = 0

        for dir in sliding[p.lower()]:
            count = 0
            while True:
                nextIndex = index + (count + 1) * dir
                if np.any(nextIndex < 0) \
                    or np.any(nextIndex >= 8) \
                    or self.boardArray[nextIndex[0], nextIndex[1]] != '-':
                    break
                count += 1
            feature[i] = count / float(8)
            i += 1

        return feature


    def buildBoardArray(self):
        fen = self.board.fen()
        boardArray = np.chararray((8,8))
        boardArray[:] = '-'
        i = j = 0
        for c in fen:
            if c.isalpha():
                boardArray[i, j] = c
                j+= 1
            elif c.isdigit():
                j += int(c)
            elif c == '/':
                j =0
                i+= 1
            elif c == ' ':
                break
        return boardArray

    def getPieceCentricFeatures(self):
        feature = np.zeros(208)
        i = 0

        #Info for each piece
        #5 for each or 32 piece (exist, x, y, attkr and defndf)
        #4 for each rook and bishop mobility 
        #8 for each queen mobility
        # => 208 features
        for piece, c in pieces.items():
            for p in (piece.lower(), piece.upper()):
                indices = np.argwhere(self.boardArray == bytes(p,encoding='utf-8'))
                for n in range(c):
                    #exist
                    exists = len(indices) > n
                    feature[i] = int(exists)
                    i += 1

                    #position
                    feature[i] = 0 if not exists else indices[n][0] / float(8)
                    i += 1

                    feature[i] = 0 if not exists else indices[n][1] / float(8)
                    i += 1

                    #attacker and defender
                    if exists:
                        attacker, defender = self.getLowestAttackerDefender(indices[n])
                        feature[i] = attacker
                        i += 1
                        feature[i] = defender
                        i += 1
                    else:
                        feature[i] = 0
                        i += 1
                        feature[i] = 0
                        i += 1

                    #mobility
                    if p.lower() in sliding:
                        feature[i:i+len(sliding[p.lower()])] = 0 if not exists else \
                            self.getPieceMobility(indices[n], p)
                        i += len(sliding[p.lower()])

        return feature

    def getGlobalFeatures(self):
        fen = self.board.fen().split(' ')[0]
        feature = np.zeros(37)
        i = 0

        #turn - 1 value
        feature[i] = int(self.board.turn)
        i += 1

        #castling right - 4 value
        feature[i] = int(self.board.has_queenside_castling_rights(True))
        i += 1
        feature[i] = int(self.board.has_kingside_castling_rights(True))
        i += 1
        feature[i] = int(self.board.has_queenside_castling_rights(False))
        i += 1
        feature[i] = int(self.board.has_kingside_castling_rights(False))
        i += 1

        #Piece count for both sides - 32 values
        for p, c in pieces.items():
            feature[i] = fen.count(p.lower()) / float(c)
            i += 1
            feature[i] = fen.count(p.upper()) / float(c)
            i += 1

        return feature

    # get the hightest value attacker for white and black for each square on the board
    # 8*8*2 = 128 feature
    def getSquareCentricFeature(self):
        feature = np.zeros(128)
        i = 0
        for r in range(8):
            for c in range(8):
                attacker, defender = self.getLowestAttackerDefender([r,c], True)
                feature[i] = attacker
                i += 1
                feature[i] = defender
                i += 1
        return feature

    def getBoardFeature(self):
        feature = np.zeros(373)
        i = 0
        feature[i:i+37] = self.getGlobalFeatures()
        i += 37
        feature[i:i+208] = self.getPieceCentricFeatures()
        i += 208 
        feature[i:i+128] = self.getSquareCentricFeature()

        return feature

if __name__ == "__main__":
    # board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/8/5NP1/PPPPPP1P/RNBQKB1R b KQkq - 1 2")
    # sqID = chess.Move.from_uci("e4a2").from_square
    board = chess.Board()
    s = State(board)

    print(s.getBoardFeature())
    