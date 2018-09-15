# -*- coding: UTF-8 -*-

# Copyright 2016 Google Inc.
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
import logging
import webapp2

import domain

GOOGLE_ASSISTANT_WELCOME_INTENT = u'Google Assistant Welcome Intent'
ASK_CONTINUE_INTENT = u'Ask Continue Intent'
ASK_WORD_INTENT = u'Ask Word Intent'
DECLARE_GOOGLE_HOME_LOSE_INTENT = u'Declare Google Home Lose Intent'


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(u'Hello, World!')

    def post(self):
        json_data = self.request.body
        obj = json.loads(json_data)
        logging.info(json.dumps(obj))

        # responseId = obj['responseId']
        # session = obj['session']
        queryResult = obj[u'queryResult']
        intentDisplayName = queryResult[u'intent'][u'displayName']

        self.response.headers['Content-Type'] = 'application/json'
        if intentDisplayName == GOOGLE_ASSISTANT_WELCOME_INTENT:
            obj = domain.ask_continue(obj)
        elif intentDisplayName == ASK_CONTINUE_INTENT:
            obj = domain.set_continue(obj)
        elif intentDisplayName == ASK_WORD_INTENT:
            obj = domain.response_word(obj)
        elif intentDisplayName == DECLARE_GOOGLE_HOME_LOSE_INTENT:
            obj = domain.response_lose_word(obj)
        else:
            obj = {
                u'fulfillmentText': queryResult[u'queryText'],
            }

        self.response.write(json.dumps(obj).encode('utf-8'))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
