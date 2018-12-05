# -*- coding: UTF-8 -*-

# Copyright 2018 [name of copyright owner]
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

from google.appengine.ext import testbed

import unittest

import infra
import domain


class TestDomain(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_response_searched_word_1(self):
        user = infra.load_user(u'TestId')

        obj = domain.response_searched_word(u'りんご', u'リンゴ', u'ja', user)

        assert obj[u'fulfillmentText'][-4] == u'、'
        assert obj[u'fulfillmentText'][-3] == u'の'
        assert obj[u'fulfillmentText'][-2] == u'、'

    def test_response_searched_word_2(self):
        user = infra.load_user(u'TestId')

        obj = domain.response_searched_word(u'ほげほげ', u'ホゲホゲ', u'ja', user)

        assert obj[u'fulfillmentText'] == u'それは知らない言葉です'
