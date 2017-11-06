import os
import datetime
import requests
from pybotframework.memory import UserMemory

import flask
import json
import tempfile
from flask import (Flask, Response, jsonify)
from flask_compress import Compress
from flask_oidc import OpenIDConnect


class BotFramework(object):
    def __init__(
        self,
        connectors,
        name=None,
        server=None,
        app_url=None,
        app_client_id=None,
        app_client_secret=None,
        oidc_client_secrets_path=None,
        message_url_pattern='api/messages',
        url_base_pathname='/',
        csrf_protect=True
    ):
        self.connectors = connectors

        self.session = requests.Session()
        self.app_client_id = app_client_id or os.environ.get('APP_ID', '')
        self.app_client_secret = app_client_secret or \
            os.environ.get('APP_PASSWORD', '')
        self.auth_str = None

        # allow users to supply their own flask server
        if server is not None:
            self.server = server
        else:
            if name is None:
                name = 'botframework'
            self.server = Flask(name)
            self.server.config['DEBUG'] = True

        self.oidc_client_secrets_path = oidc_client_secrets_path
        self.server.config.update(self._config())
        self.oidc = OpenIDConnect(self.server)

        self.message_url_pattern = message_url_pattern
        self.url_base_pathname = url_base_pathname

        # list of dependencies
        self.callback_map = {}

        # gzip
        Compress(self.server)

        # urls
        # This is kind of funky but should work
        view_func = self.oidc.accept_token()(self.handle_messages)

        self.server.add_url_rule(
            '{}{}'.format(url_base_pathname, message_url_pattern),
            view_func=view_func,
            methods=['post']
        )

    def _config(self):
        if self.oidc_client_secrets_path is None:
            f = tempfile.NamedTemporaryFile(mode='w', delete=False)
            oidc_client_secrets = {"web": {
                "client_id": self.app_client_id,
                "client_secret": self.app_client_secret,
                "redirect_uris": ["https://localhost:8080/oidc_callback"],
                "token_uri": "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token",
                "token_introspection_uri": "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token",
                "auth_uri": "https://login.botframework.com/v1/.well-known/openidconfiguration",
                "userinfo_uri": "https://login.botframework.com/v1/.well-known/openidconfiguration",
                "issuer": "https://api.botframework.com",
                "grant_type": "client_credentials",
                "scope": "https://api.botframework.com/.default"
                }
            }

            f.write(json.dumps(oidc_client_secrets))
            client_secrets_path = f.name
        else:
            client_secrets_path = self.oidc_client_secrets_path

        # TODO: Add config details here for flask app
        return {'OIDC_CLIENT_SECRETS': client_secrets_path,
                'OIDC_SCOPES': ["https://api.botframework.com/.default", "openid"],
                'OIDC_RESOURCE_SERVER_ONLY': True,
                'OIDC_INTROSPECTION_AUTH_METHOD': 'bearer'}

    def handle_messages(self):
        if flask.request.method == "POST":
            # User message to bot
            data = flask.request.json

            self.receive(data)

            return Response(
                mimetype='application/json',
                status=202
            )

        return jsonify({'message': "Invalid request method"}), 405, {
            'Content-Type': 'application/json'
        }

    def run_server(self,
                   port=6379,
                   debug=False,
                   threaded=True,
                   **flask_run_options):
        self.server.run(port=port, debug=debug, **flask_run_options)

    def receive(self, data, *args, **kwargs):
        if data["type"] == "conversationUpdate":
            # Add the members to the conversation
            self.begin_dialog(data)
        else:
            # The bot responds to the user, looking at kwargs in
            # case of added intent
            intent = None
            if 'intent' in kwargs:
                intent = kwargs['intent']
            self.respond_to_client(data, intent=intent)

    def begin_dialog(self, data):
        self.members_added = data["membersAdded"]
        member_added = self.members_added[0]["name"]
        from_id = data["from"]["id"]
        general_id = data["id"]
        sender_id = data["recipient"]["id"]

        message = ''
        for member in self.members_added:
            message += '{} added!'.format(member["name"])

        self.send(
            data["serviceUrl"],
            data["channelId"],
            general_id,
            {"id": sender_id, "name": member_added},
            {"id": from_id},
            message,
            "message",
            data["conversation"])

    def process_message(self, message, intent=None, memory=None, conn_itr=None,
                        *args, **kwargs):
        message = message.rstrip(".! \n\t")

        # Structure message in dict for handling by connector
        # (TODO: manage entire message stack)
        data = {}
        data['message'] = message

        if conn_itr is None:
            conn_itr = self.connectors.__iter__()

        # One connector response feeds into the next in this recursive function
        def resp(conndata, conn_current=None, cb=None):
            try:
                if conn_current is not None:
                    conn_prev, conn_current = conn_current, next(conn_itr)
                else:
                    conn_prev, conn_current = None, next(conn_itr)
                conndata = conn_current.respond(message)
                # Call this function recursively to pass through steps
                return resp(conndata, conn_current)
            except StopIteration as e:
                # End of steps reached
                return conndata

        # Final data
        data = resp(data)

        if data is None:
            response_message = "I didn't catch that.  One more time?"
        else:
            response_message = data

        memory.append([message, response_message])
        return response_message

    def get_auth_str(self):
        # Authentication: retrieving token from MSA service to help
        #     verify to BF Connector service
        url = "https://login.microsoftonline.com/botframework.com/"\
            "oauth2/v2.0/token"
        data = {"grant_type": "client_credentials",
                "client_id": self.app_client_id,
                "client_secret": self.app_client_secret,
                "scope": "https://api.botframework.com/.default"}
        response = requests.post(url, data)
        resp_data = response.json()
        try:
            self.auth_str = "{} {}".format(resp_data["token_type"],
                                           resp_data["access_token"])
        except KeyError:
            print("Can't create auth string: {}".format(resp_data))
            self.auth_str = ""

    def send(self, service_url, channel_id, reply_to_id,
             from_data, recipient_data, message, message_type,
             conversation):

        if not self.auth_str:
            self.get_auth_str()

        url = service_url + \
            "/v3/conversations/{}/activities/{}".format(conversation["id"],
                                                        reply_to_id)

        requests.post(
            url=url,
            json={
                "type": message_type,
                "text": message,
                "locale": "en-US",
                "from": from_data,
                "timestamp": datetime.datetime.now()
                .strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
                "localTimestamp": datetime.datetime.now()
                .strftime("%Y-%m-%dT%H:%M:%S.%f%zZ"),
                "replyToId": reply_to_id,
                "channelId": channel_id,
                "recipient": recipient_data,
                "conversation": conversation
                },
            headers={
                "Authorization": self.auth_str,
                "Content-Type": "application/json"
            }
        )

    def get_user_memory(self, data):
        """
        This method saves conversation data to UserMemory stores
        and returns the UserMemory object.
        """
        user_id = data["from"]["id"]
        channel_id = data["channelId"]
        base_url = data["serviceUrl"]
        if not self.auth_str:
            self.get_auth_str()
        user_mem = UserMemory(self.session, user_id, channel_id,
                              self.auth_str, base_url=base_url)
        return user_mem

    def respond_to_client(self, data, *args, **kwargs):
        member_added = self.members_added[0]["name"]
        general_id = data["id"]
        message = data["text"]
        sender_id = data["recipient"]["id"]

        memory = self.get_user_memory(data)

        # If there's a LUIS intent involved send off to LUISBot method
        intent = kwargs['intent']

        result = self.process_message(message=message, intent=intent,
                                      memory=memory)

        self.send(
            data["serviceUrl"],
            data["channelId"],
            general_id,
            {"id": sender_id, "name": member_added},
            {"id": data["from"]},
            result,
            "message",
            data["conversation"])
