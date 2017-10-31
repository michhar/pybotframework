from pybotframework.connector import Connector
import re
import json
import random


class RegexConnector(Connector):

    def __init__(self, intent_file, response_file):
        """
        Constructor.

        Parameters
        ----------
        model_file : str
            The file with the json dialog logic.

        """
        self.intent_list = json.load(open(intent_file, 'r'))
        self.response_dict = json.load(open(response_file, 'r'))
        super(RegexConnector, self).__init__()

    def _process(self, message):
        """
        Process the message data, reformating it so that the model will
        understand it.

        Returns
        -------
        dict
        """
        for item in self.intent_list:
            match = re.match(item['pattern'], message)
            if match:
                return (item['intent'], match.groups())
        return (None, None)

    def _postprocess(self, intent_tuple):
        """
        Read in the processed message data, pass it to the model object, and
        make a prediction. Return the data dictionary with the prediction
        added to it.

        Returns:
        -------
        dict
        """
        # Return the response to the first occurrence of the pattern in user
        # message
        (intent, entities) = intent_tuple
        response_list = self.response_dict.get(intent)
        if response_list:
            response = random.choice(response_list['messages'])
            if entities:
                response = response.format(*entities)
        else:
            response = "Could not figure out a proper response. Please try again."
        return response
