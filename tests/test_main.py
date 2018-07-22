# -*- coding: UTF-8 -*-

# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import unittest
import webtest

import main


class TestWebApp(unittest.TestCase):
    def test_get(self):
        app = webtest.TestApp(main.app)

        response = app.get('/')

        assert response.status_int == 200
        assert response.body == 'Hello, World!'

    def test_post_google_assistant_welcome_intent(self):
        app = webtest.TestApp(main.app)

        response = app.post_json(
            '/',
            {
                'queryResult':
                {
                    "intent": {
                        "displayName": "Google Assistant Welcome Intent",
                    },
                    'queryText': 'test code',
                    'languageCode': 'ja',
                }
            },
        )
        obj = json.loads(response.body)

        assert response.status_int == 200
        assert obj['followupEventInput']['name'] == 'ASK_CONTINUE_EVENT'
        assert obj['followupEventInput']['languageCode'] == 'ja'

    def test_post_ask_continue_intent(self):
        app = webtest.TestApp(main.app)

        response = app.post_json(
            '/',
            {
                'queryResult':
                {
                    "intent": {
                        "displayName": "Ask Continue Intent",
                    },
                    'queryText': 'test code',
                    'languageCode': 'ja',
                }
            },
        )
        obj = json.loads(response.body)

        assert response.status_int == 200
        assert obj['followupEventInput']['name'] == 'ASK_WORD_EVENT'
        assert obj['followupEventInput']['languageCode'] == 'ja'

    def test_post_ask_word_intent_1(self):
        app = webtest.TestApp(main.app)

        response = app.post_json(
            '/',
            {
                'queryResult':
                {
                    "intent": {
                        "displayName": "Ask Word Intent",
                    },
                    'queryText': 'ASK_WORD_EVENT',
                    'languageCode': 'ja',
                }
            },
        )
        obj = json.loads(response.body)

        assert response.status_int == 200
        assert obj['fulfillmentText'] == u'しりとり、の、り'

    def test_post_ask_word_intent_2(self):
        app = webtest.TestApp(main.app)

        response = app.post_json(
            '/',
            {
                'queryResult':
                {
                    "intent": {
                        "displayName": "Ask Word Intent",
                    },
                    'queryText': u'りんご',
                    'languageCode': 'ja',
                }
            },
        )
        obj = json.loads(response.body)

        assert response.status_int == 200
        assert obj['fulfillmentText'][-4] == u'、'
        assert obj['fulfillmentText'][-3] == u'の'
        assert obj['fulfillmentText'][-2] == u'、'

    def test_post_ask_word_intent_3(self):
        app = webtest.TestApp(main.app)

        response = app.post_json(
            '/',
            {
                'queryResult':
                {
                    "intent": {
                        "displayName": "Ask Word Intent",
                    },
                    'queryText': u'ほげほげ',
                    'languageCode': 'ja',
                }
            },
        )
        obj = json.loads(response.body)

        assert response.status_int == 200
        assert obj['fulfillmentText'] == u'それは知らない言葉です'
