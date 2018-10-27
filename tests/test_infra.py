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

import unittest

import infra


class TestInfra(unittest.TestCase):
    def test_search_reading_from_dic(self):
        json_dic = infra.load_dic(u'data/dict.json')
        reading = infra.search_reading_from_dic(u'リンゴ', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'りんご', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'林檎', json_dic)
        assert reading[u'key'] == u'リンゴ'

    def test_search_reading_from_dic_none_words(self):
        json_dic = infra.load_dic(u'data/dict.json')
        assert infra.search_reading_from_dic(u'溝口', json_dic) == {}
