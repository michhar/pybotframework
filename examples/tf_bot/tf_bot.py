from pybotframework.botframework import BotFramework
from pybotframework.tf_connector import TensorFlowConnector


tf_conn = TensorFlowConnector(model_file='model.ckpt')

my_app = BotFramework(connectors=[tf_conn])

if __name__ == '__main__':
    """Uses a trained, word2vec model to predict analogies."""
    my_app.run_server(host='0.0.0.0', port=3978, debug=True)
