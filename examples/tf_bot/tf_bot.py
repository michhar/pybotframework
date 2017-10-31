from pybotframework.botframework import BotFramework
from pybotframework.tf_connector import TensorFlowConnector


tf_conn = TensorFlowConnector(model_file='model.ckpt', word2vec_ops_fpath='../../pybotframework/word2vec/')

my_app = BotFramework(connectors=[tf_conn],
                      oidc_client_secrets_path='oidc_client_secrets.json')

if __name__ == '__main__':
    """Uses a trained, word2vec model to predict analogies."""
    my_app.run_server(host='localhost', port=3978, debug=True)
