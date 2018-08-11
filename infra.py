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

from google.appengine.ext import ndb

import json
import random

with open('data/dict.json') as json_file:
    json_dic = json.load(json_file)


class User(ndb.Model):
    words = ndb.TextProperty()
    last_word = ndb.TextProperty()
    count = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


def reset_datastore(user_id):
    try:
        user = User.get_by_id(user_id)
        user.key.delete()
    except Exception:
        pass


def get_last_word_datastore(user_id):
    try:
        user = User.get_by_id(user_id)
        if user.last_word == u'':
            return u'リ'
        return user.last_word[-1]
    except Exception:
        return u'リ'


def check_last_word_datastore(user_id, check_word):
    try:
        if check_word[0] == get_last_word_datastore(user_id):
            return True
        return False
    except Exception:
        return True


def check_word_datastore(user_id, check_word):
    try:
        user = User.get_by_id(user_id)
        words = user.words.split(u',')
        if check_word in words:
            return False
        return True
    except Exception:
        return True


def save_word_datastore(user_id, save_word):
    try:
        user = User.get_by_id(user_id)
        user.words += u',' + save_word
        user.count += 1
    except Exception:
        user = User(id=user_id)
        user.words = save_word
        user.count = 1
    user.last_word = save_word
    user.put()


def search_reading_from_dic(search_word):
    """json形式の辞書ファイルを全探索し、引数の文字列の読みをカタカナで返す

    :param unicode search_word: 検索する文字列
    :rtype: unicode
    :return: 検索した文字列のカタカナ読み(辞書にない場合は'')
    """
    for dict_record in json_dic:
        for word in dict_record[u'org']:
            if word == search_word:
                return dict_record[u'key']
    return u''


def search_word_record_from_dic(user_id, search_first):
    """json形式の辞書ファイルを全探索し、読みが search_first で始まる適当な単語レコードを返す。
    無効な単語（既出の単語・存在しない単語・「ん」で終わる単語）のレコードは返さない。

    :param unicode search_first: カタカナ 1 文字
    :rtype: dict
    :return: 検索した単語レコード(辞書にない場合は空の辞書)
    """
    dict_record_list = []
    for dict_record in json_dic:
        # search_first で始まる単語レコードを検索する
        if dict_record[u'first'] != search_first:
            continue
        # 「ん」で終わる単語は除外する
        if dict_record[u'end'] == u'ン':
            continue
        # Google Home は既出の単語を言わない
        if not check_word_datastore(user_id, dict_record[u'key']):
            continue
        dict_record_list.append(dict_record)
    if dict_record_list:
        return dict_record_list[random.randint(0, len(dict_record_list) - 1)]
    else:
        return {}
