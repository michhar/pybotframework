"""
Invoking py.test:
    Running quietly:
        py.test -q pybotframework/test/test_luis.py
    Printing to console:
        py.test -s pybotframework/test/test_luis.py
"""

# import pytest
import os
from pybotframework.luis_connector import LUISConnector
from pprint import pprint


def test_luis():
    luis_object = LUISConnector()
    luis_object.get_app_id()
    luis_object.get_app_key()
    luis_object.get_app_url()
    assert luis_object.get_app_id() == os.environ.get('LUIS_APP_ID')
    assert luis_object.get_app_key() == os.environ.get('LUIS_APP_KEY')
    assert isinstance(luis_object.url, str)
    assert luis_object.get_verbose() == 'true'
    assert luis_object.get_staging() == 'true'
    luis_object.set_staging(False)
    luis_object.set_verbose(False)
    assert luis_object.get_verbose() == 'false'
    assert luis_object.get_staging() == 'false'
    luis_object.set_staging(True)
    luis_object.set_verbose(True)
    assert luis_object.get_verbose() == 'true'
    assert luis_object.get_staging() == 'true'
    # pytest.set_trace()
    data = {'text': 'news in paris'}
    query = luis_object.query_luis(data)
    pprint(query)
    query_keys = query.keys()
    query_keys_to_check = ['intents', 'entities', 'best_intent']
    for key in query_keys:
        assert key in query_keys_to_check
    best_intent = query['best_intent']
    assert isinstance(best_intent.intent, str)
    assert isinstance(best_intent.score, float)
    entities = query['entities']
    assert isinstance(entities, list)
    assert isinstance(entities[0].entity, str)
    assert isinstance(entities[0].type, str)
    assert isinstance(entities[0].score, float)
    assert isinstance(entities[0].start_index, int)
    assert isinstance(entities[0].end_index, int)
    intents = query['intents']
    assert isinstance(intents, list)
    assert isinstance(intents[0].intent, str)
    assert isinstance(intents[0].score, float)
    processed_message = luis_object.process_message(data)
    assert isinstance(processed_message, str)
    print(processed_message)
