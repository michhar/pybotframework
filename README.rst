Python Bot Framework Wrapper
--------

Description:  Python wrapper/package for Bot Framework REST API and State REST API (package in initial phases)

To use (this will do more soon), simply do::

    >>> import pybotframework

Notes on how the example bot works with this package currently (in fact it doesn't use this package at the moment), however it does use the following tools:

Redis_ is used here as an in-memory data structure store and message broker.

.. _Redis: https://redis.io/

Celery_ is used for asynchronous task queues and scheduling in combination with flask.

.. _Celery: http://www.celeryproject.org/

Flask_ is the web app framework used here for message routing and where all of the bot logic is written.

.. _Flask: http://flask.pocoo.org/

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
** Docker (if macOS get https://docs.docker.com/docker-for-mac/install/ and if Windows get https://docs.docker.com/docker-for-windows/install/)
** Ngrok https://ngrok.com/download
** C/C++ compiler (gcc/g++) for TensorFlow bot (Windows http://mingw-w64.org/doku.php/download/mingw-builds, Mac type ‘g++’ in the terminal and follow instructions)
** Some knowledge of ML and neural nets (optional)



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

    cd <pybotframework directory>
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
