import collections
import numpy as np
import os
import tensorflow as tf
import urllib.request
import zipfile
from pybotframework.connector import Connector


class TensorFlowConnector(Connector):
    """
    TensorFlow connector. This connector uses the Word2Vec model (Mikolov et al.) to predict analogies. The Word2Vec
    model creates word embeddings, which is a way of representing relationships between words using vectors. Using
    the model, the TensorFlowConnector predicts words that are similar to a given word.
    """

    def __init__(self, model_file):
        Connector.__init__(self)
        self.model_path = '/'.join(os.getcwd().split('/')[0:-2])+'/examples/tf_bot/data'
        if len(os.getcwd().split('/')) == 1:
            self.model_path = '\''.join(os.getcwd().split('\'')[0:-2]) + '/examples/tf_bot/data'
        self.model = os.path.join(self.model_path, model_file)
        self.sess = None
        self.graph = tf.Graph()
        self.vocab_size = 10000
        self.valid_examples = np.arange(self.vocab_size)
        self.valid_window = 100
        self.batch_size = 128
        self.embedding_size = 128

    def read_data(self, filename):
        """
        Extract the first file enclosed in a zip file as a list of words.

        :param: filename: str: Name of the zipped file used for training.
        :returns: list
        """
        with zipfile.ZipFile(filename) as f:
            data = tf.compat.as_str(f.read(f.namelist()[0])).split()

        return data

    def maybe_download(self, filename, url, expected_bytes):
        """
        Download a file if not present, and make sure it's the right size.

        :param: filename: str: Name of the zipped file used for training.
        :param: url: str: URL address for zipped file.
        :param: expected_bytes: int: Number of expected bytes in the file
        :returns: str
        """
        if not os.path.exists(filename):
            filename, _ = urllib.request.urlretrieve(url + filename, filename)
        statinfo = os.stat(filename)
        if statinfo.st_size == expected_bytes:
            pass
        else:
            raise Exception(
                'Failed to verify ' + filename + '. Can you get to it with a browser?')
        return filename

    def build_dataset(self, words, n_words):
        """
        Process raw inputs into a dataset.

        :param: words: Data extracted from zipped, text file used for training.
        :param:  n_words: int: Number of words to train on.
        :returns: list, int, dict, dict
        """
        count = [['UNK', -1]]
        count.extend(collections.Counter(words).most_common(n_words - 1))
        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)
        data = list()
        unk_count = 0
        for word in words:
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK']
                unk_count += 1
            data.append(index)
        count[0][1] = unk_count
        reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        return data, count, dictionary, reversed_dictionary

    def collect_data(self, vocabulary_size=10000):
        """
        Read data and create the dictionary

        :param: vocabulary_size: int: Number of words to train on.
        :returns: list, int, dict, dict
        """
        url = 'http://mattmahoney.net/dc/'
        filename = self.maybe_download('text8.zip', url, 31344016)
        vocabulary = self.read_data(filename)
        data, count, dictionary, reverse_dictionary = self.build_dataset(vocabulary, vocabulary_size)
        del vocabulary  # Hint to reduce memory.
        return data, count, dictionary, reverse_dictionary

    def _preprocess(self, message):
        """
        Clean up the bot message.

        :param message: str: Message read from the bot.
        :returns: list
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
        :returns: str
        """

        data, count, dictionary, reverse_dictionary = self.collect_data(vocabulary_size=self.vocab_size)

        input_word = message[-1]

        # Reinitialize things
        with self.graph.as_default():

            # Input data.
            train_inputs = tf.placeholder(tf.int32, shape=[self.batch_size])
            train_context = tf.placeholder(tf.int32, shape=[self.batch_size, 1])
            valid_dataset = tf.constant(self.valid_examples, dtype=tf.int32)

            # Look up embeddings for inputs.
            embeddings = tf.Variable(
                tf.random_uniform([self.vocab_size, self.embedding_size], -1.0, 1.0))
            embed = tf.nn.embedding_lookup(embeddings, train_inputs)

            # Compute the cosine similarity between minibatch examples and all embeddings.
            norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
            normalized_embeddings = embeddings / norm
            valid_embeddings = tf.nn.embedding_lookup(
                normalized_embeddings, valid_dataset)
            similarity = tf.matmul(
                valid_embeddings, normalized_embeddings, transpose_b=True)

            # Add variable initializer.
            init = tf.global_variables_initializer()

        with tf.Session(graph=self.graph) as session:
            saver = tf.train.Saver()
            saver.restore(session, self.model)

            sim = similarity.eval()
            if input_word in dictionary:
                idx = dictionary[input_word]
                valid_word = reverse_dictionary[idx]
                top_k = 3  # number of nearest neighbors
                nearest = (-sim[idx, :]).argsort()[1:top_k + 1]
                log_str = 'nearest words to %s are' % valid_word
                for k in range(top_k):
                    close_word = reverse_dictionary[nearest[k]]
                    log_str = '%s %s' % (log_str, close_word)
                return log_str
            else:
                return 'no match'

    def _postprocess(self, prediction):
        """
        Pass the model prediction to a sentence, generating the bot response. Return the response.

        :param prediction: str: Tensorflow model prediction.
        :return: str
        """
        if prediction != 'no match':
            return "I figured it out! The {}.".format(prediction)
        else:
            return "I'm sorry, I was unable to find any nearby words."
