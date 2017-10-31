from pybotframework.botframework import BotFramework
from pybotframework.sklearn_connector import SklearnConnector

target_names = ['neg', 'pos']

sklearn_lang_conn = SklearnConnector(model_file='sentiment.pkl',
                                     target_names=target_names)

my_app = BotFramework(connectors=[sklearn_lang_conn])

if __name__ == '__main__':
    """Created for the movie review dataset from scikit-learn tutorials
     and from a model trained with a SGDClassifier"""
    my_app.run_server(host='localhost', port=3978, debug=True)
