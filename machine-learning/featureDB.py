import numpy as np
from config import *

class FeatureDB(object):
    def __init__(self, feature, label = None):
        self.db = np.load(feature)
        self.n = self.db.shape[0]
        self.index = 0

        self.labels = label is not None
        if self.labels:
            self.db = np.hstack((self.db, np.load(label)))
        np.random.shuffle(self.db)

    def getNextBatch(self, size):
        if size > self.n:
            raise IndexError

        if self.index + size >= self.n:
            np.random.shuffle(self.db)
            self.index = 0

        if self.labels:
            feats = self.db[self.index:self.index + size, 0 : -1]
            labels = self.db[self.index:self.index + size, -1]
            labels.shape = (-1 , 1)
            self.index += size
            return feats, labels
        else:
            feats = self.db[self.index:self.index + size,  :]
            self.index += size
            return feats
    
    def getFeats(self):
        if self.labels:
            return self.db[:,:-1]
        else:
            return self.db

    def getLabels(self):
        if self.labels:
            labels = self.db[:,-1]
            labels.shape = (-1, 1)
            return labels
        else:
            return None

    def size(self):
        return self.n

if __name__ == "__main__":
    trainDB = FeatureDB(TrainFeatPath, TrainFeatPath)
    print(trainDB.getFeats())