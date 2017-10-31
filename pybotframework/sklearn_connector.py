from pybotframework.connector import Connector
from sklearn.externals import joblib

class SklearnConnector(Connector):
    """We use this as a public class for use with Scikit-learn language
    classifiers.

    You call this class before calling the constructor to the
        :mod:`botframework`

    .. note::

       Target names (labels) are specified before creating the connector with
           :func:`sklearn_connector.SklearnConnector()` in this class.

    """

    def __init__(self, model_file, target_names):
        """Instantiates the Scikit-learn language model connector.

        :param model_file:  The pickled model file.
        :type model_file: str.
        :param target_names:  List of string labels associated with the model.
        :type target_names: list.
        """
        Connector.__init__(self)
        self.target_names = target_names
        self.model = joblib.load(model_file)

    def _preprocess(self, message):
        """
        Process the message data, reformatting it so that the model will
        understand it.  This is called by this class.

        :param message: Message from user.
        :type message: str.
        :returns:  str -- the return code.
        """
        # Doesn't do anything at the moment
        return message

    def _process(self, message, userinfo=None):
        """
        Read in the processed message, pass it to the model object, and
        make a prediction.  This is called by this class.

        :param message: Cleaned message.
        :type message: str.
        :param userinfo: Additional user data (e.g. User name).
        :type userinfo: dict.
        :returns:  str -- the return code.
        """
        try:
            pred = self.model.predict([message])
            if pred is not None and len(pred) >= 0:
                # We only take the first prediction value
                return str(pred[0])
            else:
                raise Exception
        except Exception as e:
            self._handle_exception(e)

    def _postprocess(self, prediction):
        """
        Operate on the prediction from :func`process`.  Convert it
        to a valid response using the target_names or labels to decode
        the model output.  This is called in this class.

        :param prediction: Model prediction needing further processing.
        :type prediction: str.
        :returns:  str -- the return code.
        """
        try:
            # Use the specified target names (labels) to re-encode the result
            return self.target_names[int(prediction)]
        except (ValueError, IndexError) as e:
            self._handle_exception(e)

    @staticmethod
    def _handle_exception(e):
        return 'I encountered a problem: {}.'.format(str(e))

