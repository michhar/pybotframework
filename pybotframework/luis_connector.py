import luis
import os
from pybotframework.connector import Connector

APPS_PAGE = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/'


class LUISConnector(Connector):

    def __init__(self, model_file):
        super(LUISConnector, self).__init__()
        self.model = model_file
        self._app_id = os.environ.get('LUIS_APP_ID')
        self._app_key = os.environ.get('LUIS_APP_KEY')
        self.url = ''
        self.staging = 'true'  # Takes either 'true' or 'false', depending on whether app is in staging or production
        self.verbose = 'true'  # Take either 'true' or 'false'

    def get_app_id(self):
        """
        Helper function to return the Luis app id.

        :return: str
        """
        return self._app_id

    def get_app_key(self):
        """
        Helper function to return the Luis app key.

        :return: str
        """
        return self._app_key

    def get_staging(self):
        """
        Helper function to return staging value.

        :return: str
        """
        return self.staging

    def get_verbose(self):
        """
        Helper function to return verbose value.

        :return: str
        """
        return self.verbose

    def set_staging(self, value):
        """
        Function to set the staging value.

        :return: str
        """
        if value:
            self.staging = 'true'
        else:
            self.staging = 'false'

    def set_verbose(self, value):
        """
        Function to set the verbose value.

        :return: str
        """
        if value:
            self.verbose = 'true'
        else:
            self.verbose = 'false'

    def get_app_url(self):
        """
        Given the Luis app id, Luis app key, verbose value, and staging value, create the url to connect to Luis and
        return it.

        :return: str
        """
        self.url = APPS_PAGE+'{}?subscription-key={}&staging={}&verbose={}&timezoneOffset=0&q='\
            .format(self.get_app_id(), self.get_app_key(), self.get_staging(), self.get_verbose())
        return self.url

    def _preprocess(self, message):
        """
        Clean up the message and return it.

        :param message: str: Message string.
        :return: str
        """
        message = message.rstrip(".! \n\t")
        return message

    def _process(self, message, userinfo=None):
        """
        Query LUIS. Return a Luis object with intents, entities, and the best intent.

        :param message: str: Message string.
        :rtype: luis.Luis()
        """
        luis_object = luis.Luis(url=self.get_app_url())
        prediction = luis_object.analyze(message)
        return prediction

    def _postprocess(self, prediction):
        """
        Convert Luis object into a dictionary, extracting the intents, entities, and best intent. Return a message to
        the user with the best intent.

        :param prediction: luis.Luis(): Luis object returned by :func`process`.
        :rtype: str
        """
        result = dict()
        result['intents'] = prediction.intents
        result['entities'] = prediction.entities
        result['best_intent'] = prediction.best_intent().intent
        if result['best_intent'] != 'None':
            return 'You would like {}. Am I correct?'.format(result['best_intent'])
        else:
            return 'I do not understand what you want to do'

