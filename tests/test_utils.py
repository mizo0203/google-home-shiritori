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

import utils


class TestInfra(unittest.TestCase):
    def test_replace_hiragana_to_katakana(self):
        # 正常系
        assert utils.replace_hiragana_to_katakana(u'ふりがな') == u'フリガナ'
        assert utils.replace_hiragana_to_katakana(u'りんご') == u'リンゴ'

        # 異常系 - ひらがなとカナカナが混在
        assert utils.replace_hiragana_to_katakana(u'フリがな') == u'フリガナ'
        assert utils.replace_hiragana_to_katakana(u'りんゴ') == u'リンゴ'

        # 異常系 - 漢字混じり
        assert utils.replace_hiragana_to_katakana(u'振り仮名') == u'振リ仮名'
        assert utils.replace_hiragana_to_katakana(u'林檎') == u'林檎'
