.. _deploy:

==================
Deploying Your Bot
==================

Prerequisites
=============

- Account on Docker Hub
- Azure subscription

Instructions
============

Linux Web App
-------------

1.  From Azure Portal (`portal.azure.com <https://portal.azure.com>`_) spin up a Linux Web App
2.  Log in to Docker locally (``docker login`` and enter your credentials for Docker Hub)
3.  Build the docker image from the bot's Dockerfile (you can name the image anything you wish):

.. code-block:: text

    docker build -f Dockerfile -t flaskbot:latest .
    docker images

4.  Tag the image with the Docker Hub username (here, dockeruser) and tag:

.. code-block:: text

    docker tag <image id> dockeruser/flaskbot

5.  Push up the docker image to Docker Hub (takes some time):

.. code-block:: text

    docker login
    docker push dockeruser/flaskbot

6.  Specify the docker image to the Linux Web App (give the app a name, resource group and point to the image):

.. code-block:: text

    az login
    az webapp config container set --name mybotname --resource-group mybotrg --docker-registry-server-url dockeruser/flaskbot

6.  Navigate to portal and click on Docker Container in left panel to ensure the app is pulling in the correct image from Docker Hub.

7.  Check that the endpoint is working:

  - Navigate to http://<your web app name>.azurewebsites.net/api/messages and should get a Method Not Allowed http error (because GET not allowed here - but this message indicates the flask app is running)

Bot Framework Portal
--------------------

Register your bot with the Microsoft Bot Framework: `register <https://docs.microsoft.com/en-us/bot-framework/portal-register-bot>`_.

Connect it to channels as is shown in `connect <https://docs.microsoft.com/en-us/bot-framework/portal-configure-channels>`_.

Happy chatting!