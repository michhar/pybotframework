Python Bot Framework Wrapper
--------

Description:  Python wrapper and package for Bot Framework REST API and State REST API (not production ready, yet).

A snippet of a basic bot:

.. code-block:: ruby
    from pybotframework.botframework import BotFramework
    from pybotframework.regex_connector import RegexConnector

    # Instatiate the connector to custom logic
    regex_conn = RegexConnector(intent_file='regex.json', response_file='responses.json')

    # Instatiate the bot
    my_app = BotFramework(connectors=[regex_conn])

    # Run flask app on port specified here
    if __name__ == '__main__':
        my_app.run_server(host='localhost', port=3978, debug=True)


See the README in the examples folder for running a test bot.

Requirements
==========================

* Bot Framework Emulator https://github.com/Microsoft/BotFramework-Emulator
* Python installed (Anaconda 3.5 recommended) https://anaconda.org/
* Python experience https://docs.python.org/3/tutorial
* Python packages (check requirements.txt file on pybotframework repo for these)
* Pybotframework library installed from repo (python setup.py) and repo downloaded for tutorials https://github.com/michhar/pybotframework - link will be live 10/26
* Azure subscription if you wish to deploy (optional) https://azure.microsoft.com/en-us/free/
* Either Docker and Ngrok or a C/C++ compiler:
* Docker (if macOS get https://docs.docker.com/docker-for-mac/install/ and if Windows get https://docs.docker.com/docker-for-windows/install/)
* Ngrok https://ngrok.com/download
* C/C++ compiler (gcc/g++) for TensorFlow bot (Windows http://mingw-w64.org/doku.php/download/mingw-builds, Mac type ‘g++’ in the terminal and follow instructions)
* Some knowledge of ML and neural nets (optional)



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

Now build thedocker image.

    cd <pybotframework base directory>

    docker build .

    docker images
    
Search for your docker "Image ID" in the list

    docker run -p 3978:3978 -id <image ID> python

    docker ps

You should see your container ID running.

Now try to connect to the bot by entering the address:
http://localhost:3978/api/messages

You should see the messages "User added!" and "Bot added!"
This means that you are set up!


Links
========

Link to Flask project:

.. _Flask: http://flask.pocoo.org/
