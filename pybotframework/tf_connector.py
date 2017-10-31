import numpy as np
import os
import tensorflow as tf
import pybotframework.word2vec.word2vec_optimized as word2vec_optimized
from pybotframework.word2vec.word2vec_optimized import Options, Word2Vec, FLAGS
from pybotframework.connector import Connector


# Define TensorFlow flags
# FLAGS.save_path = '.'  # Save model to the current path
FLAGS.save_path = os.getcwd()  # Save model to the current path
FLAGS.train_data = '/'.join(os.getcwd().split('/')[0:-1]) + '/data/text8_trimmed.txt'  # Dataset to
#  train the model
FLAGS.eval_data = '/'.join(os.getcwd().split('/')[0:-1]) + '/data/questions-words.txt'  # A list of analogies to
# test the model


class Word2VecWrapper(Word2Vec):

    def __init__(self, options, session):
        Word2Vec.__init__(self, options, session)

    def analogy(self, w0, w1, w2):
        """Predict word w3 as in w0:w1 vs w2:w3."""
        wid = np.array([[self._word2id.get(w, 0) for w in [w0, w1, w2]]])
        idx = self._predict(wid)
        for c in [self._id2word[i] for i in idx[0, :]]:
            if c not in [w0, w1, w2]:
                return c
        return 'unknown'


class TensorFlowConnector(Connector):
    """
    TensorFlow connector. This connector uses the Word2Vec model (Mikolov et al.) to predict analogies. The Word2Vec
    model creates word embeddings, which is a way of representing relationships between words using vectors. This
    makes is useful as a tool to predict analogies between words. For examples, a) wife it to b) husband as c) queen
    is to d) ???. In this case, the Word2Vec model would predict king for d).
    """

    def __init__(self, model_file):
        Connector.__init__(self)
        self.model = os.path.join(FLAGS.save_path, model_file)
        # self.sess = None
        self.sess = tf.Session()
        self.loaded_model = None
        self.word2vec = tf.load_op_library(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                        'word2vec/word2vec_ops.so'))
        self._load_model()

    def _load_model(self):
        # Load hyperparameters, etc., from the Options class
        opts = Options()
        word2vec_optimized.word2vec = self.word2vec
        # with tf.Graph().as_default(), tf.Session() as self.sess:
        tf.global_variables_initializer().run(session=self.sess)
        # Load word2vec model
        self.loaded_model = Word2VecWrapper(opts, self.sess)
        self.loaded_model.saver.restore(self.sess, self.model)
        # with tf.Graph().as_default(), tf.Session() as self.sess:
        #     tf.global_variables_initializer().run()
        #     # Load word2vec model
        #     self.loaded_model = Word2VecWrapper(opts, self.sess)
        #     self.loaded_model.saver.restore(self.sess, self.model)

    def _preprocess(self, message):
        """
        Clean up the bot message.

        :param message: str: Message read from the bot.
        :return: list
        """
        punctuations = ".!?#$%"
        for c in punctuations:
            message = message.replace(c, '')
        message = message.split(' ')
        return message

    def _process(self, message, userinfo=None, prediction=None):
        """
        Pass message through the TensorFlow Word2Vec model. Return an analogy prediction; given A is to B as C is to D,
        predict D.

        :param message: str: Cleaned bot message.
        :param userinfo: Parameters pertinent to the user.
        :type userinfo: None or list
        :param prediction: Prediction output by model.
        :type prediction: None or string
        :return: str
        """
        # Split message into three words
        w0 = message[0]
        w1 = message[1]
        w2 = message[2]

        # with tf.Graph().as_default(), tf.Session() as self.sess:
        #     prediction = self.loaded_model.analogy(w0, w1, w2)
        prediction = self.loaded_model.analogy(w0, w1, w2)
        self.sess.close()
        return prediction

    def _postprocess(self, prediction):
        """
        Pass the model prediction to a sentence, generating the bot response. Return the response.

        :param prediction: str: Tensorflow model prediction.
        :return: str
        """
        if prediction != 'unknown':
            return "I figured it out! The fourth word should be {}.".format(prediction)
        else:
            return "I'm sorry, I was unable to find an analogy with the words you provide. Please try again."
