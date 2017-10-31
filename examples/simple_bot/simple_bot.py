from pybotframework.botframework import BotFramework
from pybotframework.regex_connector import RegexConnector

regex_conn = RegexConnector(intent_file='regex.json', response_file='responses.json')

my_app = BotFramework(connectors=[regex_conn])


if __name__ == '__main__':
    # Run flask app on port specified here
    my_app.run_server(host='localhost', port=3978, debug=True)
