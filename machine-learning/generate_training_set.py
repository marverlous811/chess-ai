import chess
import chess.pgn
import os
import csv
import time
import numpy as np
import math
from state import State
from engine import SimpleStockFish
from config import *

values = {'1/2-1/2':0, '0-1':-1, '1-0':1}
numberGame = 0

def board_print(board):
    os.system('clear')
    print(board)

def get_dataset(pgn, output = None, limit = math.inf):
    start_time = time.time()
    while 1:
        game = chess.pgn.read_game(pgn)
        global numberGame
        numberGame = numberGame + 1
        if numberGame > limit:
            break
        if game is None:
            break
        res = game.headers['Result']
        if res not in values:
            continue
        value = values[res]
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            if output is not None:
                output.writerow([board.fen()])
            # board_print(board)


def load_data(output, limit = math.inf):
    output = open(output, 'w')
    writer = csv.writer(output)

    # print(os.listdir("data"))

    for fn in os.listdir("data"):
        filepath = os.path.join("data",fn)
        print(filepath)
        pgn = open(filepath, encoding = "ISO-8859-1")
        get_dataset(pgn, writer, limit)
        pgn.close()
        if numberGame > limit:
            break
    
    output.close()

def shuffleCSV(inputFile, outputFile):
    lines = open(inputFile, 'rb').readlines()
    random.shuffle(lines)
    open(outputFile, 'wb').writelines(lines)

def buildLabelDB(fenFile, output, evalFunc):
    with open(fenFile, 'rb') as f:
        fenstrings = np.array(f.readlines())
        labelArray = np.empty((len(fenstrings), 1))
        for index, s in enumerate(fenstrings):
            labelArray[index, :] = evalFunc(chess.Board(s.decode("utf-8")))
    np.save(output, labelArray)

def buildFeatureDB(fenFile, output):
    with open(fenFile, "rb") as f:
        fenstrings = np.array(f.readlines())
        featArray = np.empty((len(fenstrings), 373))
        for index, s in enumerate(fenstrings):
            _state = State(chess.Board(s.decode("utf-8")))
            featArray[index,:] = _state.getBoardFeature()
    
    np.save(output, featArray)

def sliceTestData(db, train, test, testRatio):
    data = np.load(db)
    cutoff = int(data.shape[0] * testRatio)
    np.save(train, data[:-cutoff])
    np.save(test, data[-cutoff:])

def sliceTestBoards(boardDB, trainOut, testOut, testRatio):
    with open(boardDB, "rb") as f:
        fenstrings = np.array(f.readlines())
        cutoff = int(fenstrings.shape[0] * testRatio)
        np.save(trainOut, fenstrings[:-cutoff])
        np.save(testOut, fenstrings[-cutoff:])
        print(fenstrings[0])


if __name__ == "__main__":
    # pgn = open(os.path.join("data/KingBase2019-B20-B49.pgn"))
    # get_dataset(pgn)
    load_data(FenDBPath, limit=TotalGame)

    buildFeatureDB(FenDBPath, FeatDBPath)

    engine = SimpleStockFish(depth=Depth)
    buildLabelDB(FenDBPath, LabelDBPath, engine.evaluate)

    sliceTestData(FeatDBPath, TrainFeatPath, TestFeatPath, .2)
    sliceTestData(LabelDBPath, TrainLabelPath, TestLabelPath, .2)

    sliceTestBoards(FenDBPath, TrainBoard, TestBoard, .2)