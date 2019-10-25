import tensorflow as tf
import numpy as np
from featureDB import *

tf.compat.v1.disable_eager_execution()

class Model(object):
    def __init__(self, restore = None):
        self.trainDB = None
        self.testDB = None

        self.x = tf.compat.v1.placeholder(tf.float32, shape=[None, 373])
        self._y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])

        self.y = self.buildNetwork(self.x)

        self.cost = tf.compat.v1.reduce_mean(tf.abs(tf.subtract(self.y, self._y)))
        self.optimizer = tf.compat.v1.train.AdamOptimizer().minimize(self.cost)

        # Add ops to save and restore all the variables.    
        self.saver = tf.compat.v1.train.Saver()
        # Operation to initialize the variables
        self.init = tf.compat.v1.global_variables_initializer()

        # Start session
        self.sess = tf.compat.v1.Session()
        if restore is not None:
            self.saver.restore(self.sess, restore)
            print("Checkpoint ", restore, " restored")
        else:
            self.sess.run(self.init)
            print("initialized variables")

    def buildNetwork(self, x):
        feature_init = tf.random_normal_initializer(stddev=0.35)
        globalW = tf.Variable(initial_value=feature_init(shape=(37, 20)), name="globalW")
        globalB = tf.Variable(initial_value=feature_init(shape=(20,)), name="globalB")
        piecesW = tf.Variable(initial_value=feature_init(shape=(208, 100)), name="piecesW")
        piecesB = tf.Variable(initial_value=feature_init(shape=(100,)), name="pieceB")
        squareW = tf.Variable(initial_value=feature_init(shape=(128, 50)), name="squareW")
        squareB = tf.Variable(initial_value=feature_init(shape=(50,)), name="squareB")

        w2 = tf.Variable(initial_value=feature_init(shape=(170, 75)), name="W2")
        b2 = tf.Variable(initial_value=feature_init(shape=(75,)), name="B2")

        w3 = tf.Variable(initial_value=feature_init(shape=(75, 1)), name="W3")
        b3 = tf.Variable(initial_value=feature_init(shape=(1,)), name="B3")

        #first layer
        globalOutput = tf.add(tf.matmul(tf.slice(x, [0,0], [-1, 37]), globalW), globalB)
        piecesOutput = tf.add(tf.matmul(tf.slice(x, [0, 37], [-1, 208]), piecesW), piecesB)
        squareOutput = tf.add(tf.matmul(tf.slice(x, [0, 37 + 208], [-1, -1]), squareW), squareB)
        layer1Output = tf.concat( [globalOutput, piecesOutput, squareOutput], 1)

        #2nd layer
        input2 = tf.nn.relu6(layer1Output)
        output2 = tf.add(tf.matmul(input2, w2), b2)

        #3rd layer
        input3 = tf.nn.relu6(output2)
        output3 = tf.add(tf.matmul(input3, w3), b3)

        return tf.tanh(output3)
    
    def runInput(self, feature):
        if(len(feature.shape) == 1):
            feature = feature.reshape(1,-1)
        return self.sess.run(self.y, feed_dict={self.x: feature})

    def getSession(self):
        return self.sess
    
    def save(self, name=''):
        save_path = self.saver.save(self.sess, name)
        print("Model saved in file: %s" % save_path)

    def setDB(self, trainDB = None, testDB = None):
        self.trainDB = trainDB
        self.testDB = testDB

    def train(self, batchSize=1000, epochs=50, displayStep=1):
        if self.trainDB is None:
            print("not have data to train")
            return
        dbSize = self.trainDB.size()
        iPerE = dbSize/ batchSize

        #start training
        iteration = 0
        epoch = 0
        while epoch < epochs:
            while iteration < iPerE:
                #Get the next batch
                batch_xs, batch_ys = self.trainDB.getNextBatch(batchSize)
                #Fit training using batch data
                self.sess.run(self.optimizer, feed_dict={self.x: batch_xs, self._y: batch_ys})

                #Calculate batch loss on display steps
                if epoch % displayStep == 0 and iteration == 0:
                    batchError = self.sess.run(self.cost, feed_dict={self.x: batch_xs, self._y: batch_ys})
                    print("Epoch ", epoch, " - Minibatch Avg Error " + "{:.6f}".format(batchError))
                iteration += 1
            
            epoch += 1
            iteration = 0

        print ("Optimization Finished!")
        #Calculate accuracy for test set
        print("Testing Error: ", self.sess.run(self.cost, feed_dict={self.x: self.testDB.getFeats(), self._y: self.testDB.getLabels()}))

    def test(self):
        if self.testDB is None:
            print("not have data to test")
        print("Testing Error: ", self.sess.run(self.cost, feed_dict={self.x: self.testDB.getFeats(), self._y: self.testDB.getLabels()}))


if __name__ == "__main__":
    model = Model()
    trainDB = FeatureDB('gameDB/trainX.npy', 'gameDB/sfTrainY.npy')
    testDB = FeatureDB('gameDB/testX.npy', 'gameDB/sfTestY.npy')
    model.setDB(trainDB,testDB)
    model.train(batchSize=500)
    # print(model.runInput(trainDB.getFeats()))
    model.save('checkpoints/sfBoot.ckpt')

    # model.runInput(s.getBoardFeature())
    # model.buildNetwork(s.getBoardFeature())