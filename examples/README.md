## Examples

### `ms-pythonbot`

This example is a simple "Hi there!" python bot using the [Flask microframework](http://flask.pocoo.org/) to work with the Bot Framework on Azure or even just locally with the Bot Framework Emulator (recommended to use for testing and dev).

#### Setup

NOTE:  The flask app tests to see which OS the app is on and decides how to call the necessary dependencies.

* Download the Bot Framework Emulator for local testing (https://github.com/Microsoft/BotFramework-Emulator#download) - multiple OS compatibility.

##### Unix

1. Download redis for unix and build (https://redis.io/download)
* Change the name of the redis folder to 'redisunix' under `ms-pythonbot` root folder so that the app can find it (thus it will have `redis-server` in the path `redisunix/src`).


##### Windows


 1.  Download and set up redis for windows (https://github.com/ServiceStack/redis-windows)
 * Change the name of the windows redis to 'rediswin' (thus it will have `redis-server.exe` in the path `rediswin\`).


#### Check

Ensure celery and all packages from the requirements.txt file are installed locally or if using a virtual environment inside that environment (check Lib -> site-packages just to be sure).

#### Run

From the `ms-pythonbot` base folder:

    python runserver.py

This will start the redis server as a message broker and the celery program as a task queue.

TODO:  Keep the messages from a bot to one worker on celery

#### Test locally in emulator

1. Open up the BF Emulator (usually called `botframework-emulator` on your system)
* Click on the "Enter your endpoint URL" and select or type in `http://localhost:3978/api/messages`
* Leave the "Microsoft App ID" and "Microsoft App Password" blank
* Click "CONNECT"

You should see in the Log window a "conversationUpdate" appear twice with no errors.  If there's an error ensure you have the `runserver.py` script going.

