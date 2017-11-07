.. _introduction:

Introduction
============

Description:  Python wrapper and package for Bot Framework REST API and State REST API (not production ready, yet).


The project,``pybotframework``, provides an easy way to create intelligent Python-based chatbots. It
leverages Microsoft's Bot Framework REST APIs for easy deployment and connection to channels like Slack, Skype, FB
Messenger and more. We aimed it to have rich dialogs by providing gateways to custom trained machine learning models
and dialog logic.

It includes a great development experience due to its compatibility with an open source
`channel emulator <https://github.com/Microsoft/BotFramework-Emulator#download>`_. It also uses the familiar web
microframework, `Flask <http://flask.pocoo.org/>`_, for the web app component that can be customized later on. For
authentication it leverages `Flask-OIDC <http://flask.pocoo.org/>`_.


A snippet of a basic bot with custom ML:

.. code-block:: python

    # Labels for ML model
    target_names = ['negative', 'positive']

    # Instatiate the connector to custom ML model
    sklearn_lang_conn = SklearnConnector(model_file='sentiment.pkl',
                                         target_names=target_names)

    # Instatiate the bot
    my_app = BotFramework(connectors=[sklearn_lang_conn])


Currently the project is Python 3 compatible, with Python 2.7 support pending demand.