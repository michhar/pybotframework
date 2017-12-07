

class BotStateMachine(object):

    def __init__(self, states):
        self.states = states

    def transition_state(self, bot_state_data):
        """
        Based on the intent and entities provided, choose the next state
        """
        next_states = self.states['current_state']['next_states']
        if len(next_states) == 0:
            return self.current_state
        else:
            if bot_state_data.intent in next_states:
                return bot_state_data.intent
            else:
                return None


class BotStateData(object):
    def __init__(self, user_message,
                 intent=None,
                 entities=[],
                 bot_messages=[],
                 current_state=None,
                 next_state=None):
        self.user_message = user_message
        self.intent = intent
        self.entities = entities
        self.bot_messages = bot_messages
        self.current_state = current_state
        self.next_state = next_state
