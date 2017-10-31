"""
This file contains testing functions for use with pytest.
Run in base directory with:  python setup.py test
"""
from pybotframework.memory import (UserMemory, ConversationMemory,
                                   UserConversationMemory)

import requests
import requests_mock


# Some memory test for pytest
def test_memory():
    session = requests.Session()
    BASE_URL = 'mock://test.com'
    adapter = requests_mock.Adapter()
    session.mount('mock', adapter)

    um_url = 'mock://test.com/v3/botstate/1/users/2'
    adapter.register_uri('GET', um_url, text='{"data": []}')
    adapter.register_uri('POST', um_url, text='{"data": []}')
    um = UserMemory(session, user_id='2', channel_id='1', auth_str='',
                    base_url=BASE_URL)
    assert um.get_data() == []
    assert um_url == um.get_url()
    um.append('new data')
    adapter.register_uri('GET', um_url, text='{"data": ["new data"]}')
    assert um.get_data() == ['new data']


    cm_url = 'mock://test.com/v3/botstate/1/conversations/3'
    adapter.register_uri('GET', cm_url, text='{"data": []}')
    adapter.register_uri('POST', cm_url, text='{"data": []}')
    cm = ConversationMemory(session, conversation_id='3', channel_id='1',
                            auth_str='', base_url=BASE_URL)
    assert cm.get_data() == []
    cm.append(['new data'])
    adapter.register_uri('GET', cm_url, text='{"data": ["new data"]}')
    assert cm.get_data() == ['new data']


    ucm_url = 'mock://test.com/v3/botstate/1/conversations/3/users/2'
    adapter.register_uri('GET', ucm_url, text='{"data": []}')
    adapter.register_uri('POST', ucm_url, text='{"data": []}')
    ucm = UserConversationMemory(session, conversation_id='3', user_id='2',
                                 channel_id='1', auth_str='',
                                 base_url=BASE_URL)
    assert ucm.get_data() == []
    adapter.register_uri('GET', ucm_url, text='{"data": []}')
    ucm.append(['new data'])
    adapter.register_uri('GET', ucm.get_url(),
                         text='{"data": ["new data"]}')
    assert ucm.get_data() == ['new data']
