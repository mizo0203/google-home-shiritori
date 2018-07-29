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

import json

with open('data/dict.json') as json_file:
    json_dic = json.load(json_file)


def search_reading_from_dic(search_word):
    """json形式の辞書ファイルを全探索し、引数の文字列の読みをカタカナで返す

    :param unicode search_word: 検索する文字列
    :rtype: unicode
    :return: 検索した文字列のカタカナ読み(辞書にない場合は'')
    """
    for dict_record in json_dic:
        for word in dict_record[u'org']:
            if(word == search_word):
                return dict_record[u'key']
    return ''


def search_word_record_from_dic(search_first):
    """json形式の辞書ファイルを全探索し、読みが search_first で始まる適当な単語レコードを返す。

    :param unicode search_first: カタカナ 1 文字
    :rtype: dict
    :return: 検索した単語レコード(辞書にない場合は'')
    """
    for dict_record in json_dic:
        if(dict_record[u'first'] == search_first):
            # FIXME: 暫定実装 - 動作確認の都合上、読みの頭と尻は不一致とする
            if(dict_record[u'end'] != search_first):
                return dict_record
    return ''
