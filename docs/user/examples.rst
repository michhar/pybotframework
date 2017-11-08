==========
Examples
==========

Examples are the actual example bots.  Here is a listing and instructions on how to run them.

**************
Bots Available
**************

+-----------------------------------------------+-----------------------------------------------+-----------------------------------------------+
| Example                                       | Topics                                        | Link                                          |
+===============================================+===============================================+===============================================+
| Eliza bot                                     | regex json, response json                     | `Link 1`_                                     |
+-----------------------------------------------+-----------------------------------------------+-----------------------------------------------+
| Scikit-learn language bot                     | scikit-learn, sentiment analysis              | `Link 2`_                                     |
+-----------------------------------------------+-----------------------------------------------+-----------------------------------------------+
| TensorFlow word2Vec bot                       | TensorFlow, word2vec                          | `Link 3`_                                     |
+-----------------------------------------------+-----------------------------------------------+-----------------------------------------------+
| Microsoft LUIS bot                            | LUIS Cognitive Service                        | `Link 4`_                                     |
+-----------------------------------------------+-----------------------------------------------+-----------------------------------------------+

.. _Link 1: https://github.com/michhar/pybotframework/blob/master/examples/eliza_bot
.. _Link 2: https://github.com/michhar/pybotframework/blob/master/examples/lang_bot
.. _Link 3: https://github.com/michhar/pybotframework/blob/master/examples/tf_bot
.. _Link 4: https://github.com/michhar/pybotframework/blob/master/examples/luis_bot

****************
Running the Bots
****************

This example is a Regex python bot using the `Flask microframework <http://flask.pocoo.org/>`_ to work with the Bot Framework on Azure or even just locally with the Bot Framework Emulator (recommended to use for testing and dev).

Setup
=====

* Download the Bot Framework Emulator for local testing (https://github.com/Microsoft/BotFramework-Emulator#download) - multiple OS compatibility.
(For a full list of prerequisites see the main Readme on this repo :any:`../../Readme.rst`).

Run the Bot
===========

From the bot's base folder and on the command line:

    ``python <bot script name>.py``

e.g.

    ``python eliza_bot.py``

This will start the flask server.

Test Locally in Emulator
========================

1. Open up the BF Emulator (usually called `botframework-emulator` on your system)
2. Click on the "Enter your endpoint URL" and select or type in `http://localhost:3978/api/messages`
3. Leave the "Microsoft App ID" and "Microsoft App Password" blank
4. Click "CONNECT"

You should see in the Log window a "conversationUpdate" appear twice with no errors.  If there's an error ensure you have the `<bot script name>.py` script running on the command line.

Happy chatting!

Deployment
==========

Go to `Deployment <http://pybotframework.readthedocs.io/en/latest/user/deployment.html>`_ for deploy instructions.


