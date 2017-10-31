class Connector:
    """We use this as a public base class.  Customized connectors
    inherit this class as a framework for building them.

    .. note::

        Base connector class class as framework for child classes.

    """

    def __init__(self):
        """Instantiates the base connector.
        """
        pass

    def _preprocess(self, message):
        """
        This might involve cleaning up the input format, making
        everything lowercase (normalizing), removing extra things
        that we don't need, adding additional data from other
        sources (dictionary/word list), etc.

        :param message: Message.
        :type message: str.
        :returns:  str -- the return code.
        """
        cleaned_message = message
        return cleaned_message

    def _process(self, cleaned_message, userinfo=None):
        """
        Read in and operate on the cleaned message data from
        :func`_preprocess`.
        :param cleaned_message: Cleaned message.
        :type cleaned_message: str.
        :param userinfo: Additional user data (e.g. User name).
        :type userinfo: dict.
        :returns:  str -- the return code.
        """
        prediction = cleaned_message
        return prediction

    def _postprocess(self, prediction):
        """
        Operate on the prediction from :func`_process`.

        :param prediction: Cleaned message.
        :type prediction: str.
        :returns:  str -- the return code.
        """
        result = prediction
        return result

    def respond(self, message):
        """
        This is called by :mod:`botframework` in child classes.

        :param message: Cleaned message.
        :type message: str.
        :returns:  str -- the return code.
        """
        cleaned_message = self._preprocess(message)
        prediction = self._process(cleaned_message)
        result = self._postprocess(prediction)
        return result
