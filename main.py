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


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

    def post(self):
        json_data = self.request.body
        obj = json.loads(json_data)
        logging.info(json.dumps(obj))

        # responseId = obj['responseId']
        # session = obj['session']
        queryResult = obj['queryResult']
        # originalDetectIntentRequest = obj['originalDetectIntentRequest']

        self.response.headers['Content-Type'] = 'application/json'
        obj = {
                u'fulfillmentText': queryResult['queryText'],
                }
        self.response.write(json.dumps(obj).encode('utf-8'))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
