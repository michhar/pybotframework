from pybotframework.botframework import BotFramework
from pybotframework.luis_connector import LUISConnector

luis_conn = LUISConnector(model_file=None)

my_app = BotFramework(connectors=[luis_conn], oidc_client_secrets_path='oidc_client_secrets.json')

if __name__ == '__main__':
    # Run flask app on port specified here
    my_app.run_server(host='localhost', port=3978, debug=True)
