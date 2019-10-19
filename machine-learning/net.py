import tensorflow as tf
import numpy as np

# neural network model to evaluate chess board
class Model(object):
    def __init__(self, restore = None):
        #input variable and labels
        self.x = tf.placeholder(tf.float32, shape=[None, 373])
        self._y = tf.placeholder(tf.float32, shape=[None, 1])

        #output
        self.y = self.buildNetwork(self.x)

        # Build the optimizer
        self.cost = tf.reduce_mean(tf.abs(tf.sub(self.y, self._y)))
        self.optimizer = tf.train.AdamOptimizer().minimize(self.cost)

        # Add ops to save and restore all the variables.
        self.saver = tf.train.Saver()
        # Operation to initialize the variables
        self.init = tf.initialize_all_variables()

        # Start session
        self.sess = tf.Session()

        # Restore weights
        if restore is not None:
            self.saver.restore(self.sess, restore)
            print ("Checkpoint", restore, "restored")
        # Or initialize them
        else:
            self.sess.run(self.init)
            print ("Initialized variables")

    def buildNetwork(self, x):
        #weights and biases for the first hidden layer
        globalW = tf.Variable(tf.random_normal([37,20], stddev=0.35), name="globalW")
        globalB = tf.Variable(tf.random_normal([20], stddev=0.35), name="globalB")
        piecesW = tf.Variable(tf.random_normal([208, 100], stddev=0.35), name="pieceW")
        piecesB = tf.Variable(tf.random_normal([100], stddev=0.35), name="pieceB")
        squareW = tf.Variable(tf.random_normal([128, 50], stddev=0.35), name="squareW")
        squareB = tf.Variable(tf.random_normal([50], stddev=0.35), name="squareB")

        #weights and biases for the second hidden layer
        w2 = tf.Variable(tf.random_normal([170, 75], stddev = 0.35), name="W2")
        b2 = tf.Variable(tf.random_normal([75], stddev=0.35), name="B2")

        #weights and biases for the output hidden layer
        w3 = tf.Variable(tf.random_normal([75, 1], stddev = 0.35), name="W2")
        b3 = tf.Variable(tf.random_normal([1], stddev=0.35), name="B2")

        #Network opertaion

        #First layer
        globalOutput = tf.add(tf.matmul(tf.slice(x, [0,0], [-1, 37]), globalW), globalB)
        pieceOutput = tf.add(tf.matmul(tf.slice(x, [0, 37], [-1, 208]), piecesW), piecesB)
        squareOutput = tf.add(tf.matmul(tf.slice(x, [0, 37 + 208], [-1, -1]), squareW), squareB)
        layer1Output = tf.concat(1, [globalOutput, pieceOutput, squareOutput])

        #2nd layer
        layer2Input = tf.nn.relu6(layer1Output)
        layer2Output = tf.add(tf.matmul(layer2Input, w2), b2)

        #3rd layer
        layer3Input = tf.nn.relu6(layer2Output)
        layer3Output = tf.add(tf.matmul(layer3Input, w3), b3)

        return tf.tanh(layer3Output)

    # Run an input through the network
    def runInput(self, feature):
        if len(feature.shape) == 1:
            feature = feature.reshape(1, -1)
        return self.sess.run(self.y, feed_dict={self.x: feature})

    # Return the model's session
    def getSession(self):
        return self.sess

    # Save the model weights
    def save(self, name=''):
        save_path = self.saver.save(self.sess, name)
        print("Model saved in file: %s" % save_path)