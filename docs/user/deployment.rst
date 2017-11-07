.. _deploy:

==================
Deploying Your Bot
==================

Prerequisites
=============

- Account on DockerHub
- Azure subscription

Instructions
============

Linux Web App
-------------

1.  From Azure Portal (`portal.azure.com <https://portal.azure.com>`_) spin up a Linux Web App
2.  Log in to Docker locally (``docker login`` and enter your credentials for DockerHub)
3.  Build my docker image from the bot's Dockerfile

.. code-block:: text

    docker build -f Dockerfile -t flaskbot:latest .
    docker images

4.  Tag the image with the DockerHub username and tag:

.. code-block:: text

    docker tag <image id>  dockeruser/flaskbot

5.  Push up the docker image to DockerHub (takes some time):

.. code-block:: text

    docker login
    docker push dockeruser/flaskbot

6.  Specify the docker image to the Linux Web App:

.. code-block:: text

    az login
    az webapp config container set --name linux-pythonbot --resource-group ms-pythonbot --docker-registry-server-url rheartpython/flaskbot

6.  Navigate to portal and click on Docker Container in left panel to ensure the app is pulling in the correct image from DockerHub.

7.  Check that the endpoint is working:

  - Navigate to http://<your web app name>.azurewebsites.net/api/messages and should get a Method Not Allowed http error (because GET not allowed here - but this message indicates the flask app is running)

Bot Framework Portal
--------------------

