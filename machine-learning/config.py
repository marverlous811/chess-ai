StockEnginePath = '/Users/ows/Downloads/stockfish-10-mac/Mac/stockfish-10-64'

TotalGame = 1000
Depth=8
FenDBPath = 'fenDB.csv'

DBDir = 'gameDB'
FeatDBPath = DBDir + '/featDB.npy'
LabelDBPath = DBDir + '/labelDB.npy'
TrainFeatPath = DBDir + '/trainX.npy'
TrainLabelPath = DBDir + '/sfTrainY.npy'
TrainBoard = DBDir + '/trainBoards.npy'
TestFeatPath = DBDir + '/testX.npy'
TestLabelPath = DBDir + '/sfTestY.npy'
TestBoard = DBDir + '/testBoards.npy'

CheckpointPath = 'checkpoints/sfBoot.ckpt'
BatchSize=1000
Epochs=50
ModelDir='output'
DisplayStep=1