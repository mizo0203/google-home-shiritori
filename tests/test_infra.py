# -*- coding: UTF-8 -*-

# Copyright 2019 Hayato Kubo / Takanori Kondo / Satoki Mizoguchi
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

        # 正常系
        reading = infra.search_reading_from_dic(u'リンゴ', u'リンゴ', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'りんご', u'リンゴ', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'林檎', u'リンゴ', json_dic)
        assert reading[u'key'] == u'リンゴ'

        # 準正常系 - フリガナ取得失敗
        reading = infra.search_reading_from_dic(u'リンゴ', u'', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'りんご', u'', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'林檎', u'', json_dic)
        assert reading[u'key'] == u'リンゴ'

        # 準正常系 - フリガナのみ正常
        reading = infra.search_reading_from_dic(u'', u'リンゴ', json_dic)
        assert reading[u'key'] == u'リンゴ'
        reading = infra.search_reading_from_dic(u'林☆檎', u'リンゴ', json_dic)
        assert reading[u'key'] == u'リンゴ'

    def test_search_reading_from_dic_none_words(self):
        json_dic = infra.load_dic(u'data/dict.json')
        assert infra.search_reading_from_dic(u'溝口', u'ミゾグチ', json_dic) == {}
        assert infra.search_reading_from_dic(u'溝口', u'', json_dic) == {}
        assert infra.search_reading_from_dic(u'', u'ミゾグチ', json_dic) == {}
