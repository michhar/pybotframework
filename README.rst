Python Bot Framework Wrapper
--------

Description:  Python wrapper and package for Bot Framework REST API and State REST API (not production ready, yet).

A snippet of a basic bot:

.. code-block:: python

    from pybotframework.botframework import BotFramework
    from pybotframework.sklearn_connector import SklearnConnector

    # Labels for ML model
    target_names = ['neg', 'pos']

    # Instatiate the connector to custom ML model
    sklearn_lang_conn = SklearnConnector(model_file='sentiment.pkl',
                                         target_names=target_names)

    # Instatiate the bot
    my_app = BotFramework(connectors=[sklearn_lang_conn])

    if __name__ == '__main__':
        """Run the Flask app"""
        my_app.run_server(host='0.0.0.0', port=3978, debug=True)



See the README in the examples folder for running a test bot.

Installation
============

Install the pybotframework package from this repository with

    `pip install .`

or

    `python setup.py`



Requirements for Examples
==========================

* Bot Framework Emulator https://github.com/Microsoft/BotFramework-Emulator
* Python installed (Anaconda 3.5 recommended) https://anaconda.org/
* Python experience https://docs.python.org/3/tutorial
* Pybotframework library installed from repo (`python setup.py` or `pip install .`)
* Docker (if macOS get https://docs.docker.com/docker-for-mac/install/ and if Windows get https://docs.docker.com/docker-for-windows/install/)
* Ngrok https://ngrok.com/download
* Some knowledge of ML and neural nets (helpful)



Docker
========
To build and run the Docker image, first download and install Docker.
https://docs.docker.com/engine/installation/

Make sure Docker is up and running.

Next, download and install ngrok.

https://ngrok.com/

Then set up the botframework emulator.

https://docs.microsoft.com/en-us/bot-framework/debug-bots-emulator

Make sure to go through the "Install and configure ngrok" settings.
Uncheck the "Bypass ngrok for local addresses" to enable the bot to
talk with Docker.

Now build the docker image on the command line.

    cd <pybotframework base directory>

    docker build .

    docker images
    
Search for your docker "Image ID" in the list

    docker run -p 3978:3978 -id <image ID> python

    docker ps

You should see your container ID running.

Now try to connect to the bot by entering the address in the Emulator:
http://localhost:3978/api/messages

You should see the messages "User added!" and "Bot added!"
This means that you are set up!


Links
========

Link to Flask project:

    .. _Flask: http://flask.pocoo.org/
