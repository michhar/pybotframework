"""
Classes for State REST API
"""
BASE_URL = 'http://localhost:50894'


class Memory:
    """Memory class is the base class for all state types of storage."""
    def __init__(self, session, channel_id, auth_str, base_url):
        self.session = session
        self.channel_id = channel_id
        self.auth_str = auth_str
        self.data = []
        self.base_url = base_url
        self.etag = '*'

    def append(self, message_list):
        if not self.data or not isinstance(self.data, list):
            self.data = []
        self.data += message_list
        self.save_data()

    def save_data(self):
        self.session.post(
            url=self.get_url(),
            json={"eTag": self.etag,
                  "data": self.data},
            headers={"Authorization": self.auth_str,
                     "Content-Type": "application/json"}
        )

    def get_data(self):
        response = self.session.get(
            url=self.get_url(),
            headers={
                "Authorization": self.auth_str,
                "Content-Type": "application/json"
            }
        )
        json_data = response.json()
        self.data = json_data.get('data', [])
        self.etag = json_data.get('eTag')
        return self.data

    def get_url(self):
        return None


class UserMemory(Memory):
    """UserMemory holds the logic for working with user data."""
    def __init__(self, session, user_id, channel_id, auth_str, base_url):
        """
        Data can be any format for how you want to save.
        Lists or dictionaries are recommended so you can save multiple
        items for each conversation.
        """
        super(UserMemory, self).__init__(session, channel_id, auth_str,
                                         base_url)
        self.user_id = user_id
        self.get_data()

    def get_url(self):
        return self.base_url + \
            "/v3/botstate/{}/users/{}".format(self.channel_id,
                                              self.user_id)


class ConversationMemory(Memory):
    def __init__(self, session, conversation_id, channel_id,
                 auth_str, base_url):
        """
        Data can be any format for how you want to save.
        Lists or dictionaries are recommended so you can save multiple
        items for each conversation.
        """
        super(ConversationMemory, self).__init__(session, channel_id,
                                                 auth_str, base_url)
        self.conversation_id = conversation_id
        self.channel_id = channel_id
        self.get_data()

    def get_url(self):
        return self.base_url + \
            "/v3/botstate/{}/conversations/{}".format(self.channel_id,
                                                      self.conversation_id)


class UserConversationMemory(Memory):
    """ UserConversationMemory holds the logic for working with private
        user data for a specific conversation."""

    def __init__(self, session, conversation_id, user_id, channel_id,
                 auth_str, base_url):
        """
        This method calls the superclass. Data can be any format.
        """
        super(UserConversationMemory, self).__init__(session, channel_id,
                                                 auth_str, base_url)
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.get_data()

    def get_url(self):
        return self.base_url + \
            "/v3/botstate/{}/conversations/{}/users/{}"\
            .format(self.channel_id, self.conversation_id, self.user_id)


# TODO: refactor these into separate classes? Might need to share
#   These models among the different memory types
#     def message_activity(self):
#         return {
#             "conversationid": self._id,
#             "fromid": self.fromid,
#             "recipientid": self.recipientid,
#             "channelid": self.channelid,
#             "type": "message",
#             "text": self.message
#         }
#
#     def conversation_update_activity(self):
#         return {
#             "conversationid": self._id,
#             "fromid": self.sender_id,
#             "recipientid": self.recipient_id,
#             "channelid": self.channel_id,
#             "type": "conversationUpdate",
#
#             # TODO: append to conversation_data
#             "members_added": {"id": self.recipientid, "name": self.name}
#         }

# class Session:
#     """A session is the conversational model object.
#        This class is a composite of others."""
#     def __init__(self, memories=[]):
#         self.memories = memories
#
#     def get_data(self, _type):
#         for mem in self.memories:
#             if mem._type == _type:
#                 data = mem.get_data(auth_str='1')
#                 return data
#
#     def append_data(self, _type, data):
#         for mem in self.memories:
#             if mem._type == _type:
#                 print(mem.data)
#                 print(data)
#
#     def clear_data(self, _type):
#         for mem in self.memories:
#             if mem._type == _type:
#                 mem.data = None
