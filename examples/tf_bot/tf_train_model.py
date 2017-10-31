import os
import tensorflow as tf
import pybotframework.word2vec.word2vec_optimized as word2vec_optimized
from pybotframework.word2vec.word2vec_optimized import Options, Word2Vec, FLAGS

repo_path = '/Users/dave/DataScience/Projects/GitHub/pybotframework/pybotframework'  # Modify this line for you
# specific system
ops_file_path = 'word2vec/word2vec_ops.so'

word2vec_optimized.word2vec = tf.load_op_library(os.path.join(repo_path, ops_file_path))

# Define TensorFlow flags
FLAGS.save_path = '.'  # Save model to the current path
FLAGS.train_data = '../../pybotframework/data/text8_trimmed.txt'  # Dataset to train the model
FLAGS.eval_data = '../../pybotframework/data/questions-words.txt'  # A list of analogies to test the model

# Setup the TensorFlow graph and train the model
opts = Options()
with tf.Graph().as_default(), tf.Session() as session:
    with tf.device("/cpu:0"):
        model = Word2Vec(opts, session)
        model.read_analogies()
    for _ in range(opts.epochs_to_train):
        model.train()
        model.eval()
    # Save the model after training has finished
    model.saver.save(session, os.path.join(opts.save_path, "model.ckpt"),
                     global_step=model.global_step)
