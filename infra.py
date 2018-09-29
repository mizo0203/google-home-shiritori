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

# しりとりが WORDS_COUNT_LIMIT 以上続いたら AI が降参する
WORDS_COUNT_LIMIT = 10


with open('data/dict.json') as json_file:
    json_dic = json.load(json_file)


class User(ndb.Model):
    words = ndb.TextProperty()
    last_word = ndb.TextProperty()
    count = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


def load_user(user_id, default_last_word):
    try:
        user = User.get_by_id(user_id)
        if user:
            return user
    except Exception:
        pass

    user = User(id=user_id)
    user.words = None
    user.last_word = None
    user.count = 0
    user.date = None
    save_word_datastore(user, default_last_word)
    return user


def reset_datastore(user):
    try:
        user.key.delete()
        user.words = None
        user.last_word = None
        user.count = 0
        user.date = None
    except Exception:
        pass


def get_datastore(user_id):
    user = User.get_by_id(user_id)
    if user:
        obj = {u'words': user.words,
               u'last_word': user.last_word,
               u'count': user.count,
               }
        return obj
    return {}


def get_last_word_datastore(user):
    try:
        return user.last_word[-1]
    except Exception:
        pass


def check_last_word_datastore(user, check_word):
    try:
        if check_word[0] == get_last_word_datastore(user):
            return True
        return False
    except Exception:
        return True


def check_word_datastore(user, check_word):
    try:
        words = user.words.split(u',')
        if check_word in words:
            return False
        return True
    except Exception:
        return True


def save_word_datastore(user, save_word):
    try:
        if user.words:
            user.words += u',' + save_word
        else:
            user.words = save_word
        user.count += 1
    except Exception:
        pass
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


def search_word_record_from_dic(user, search_first):
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
        if not check_word_datastore(user, dict_record[u'key']):
            continue
        dict_record_list.append(dict_record)
    if dict_record_list:
        return dict_record_list[random.randint(0, len(dict_record_list) - 1)]
    else:
        return {}


def search_lose_word_record_from_dic(user, search_first):
    """json形式の辞書ファイルを全探索し、読みが search_first で始まり
    かつ、「ん」で終わる単語レコードを返す。

    :param unicode search_first: カタカナ 1 文字
    :rtype: dict
    :return: 検索した単語レコード(辞書にない場合は空の辞書)
    """
    dict_record_list = []
    for dict_record in json_dic:
        # search_first で始まる単語レコードを検索する
        if dict_record[u'first'] != search_first:
            continue
        # 「ん」で終わる単語を検索する
        if dict_record[u'end'] == u'ン':
            dict_record_list.append(dict_record)
    if dict_record_list:
        return dict_record_list[random.randint(0, len(dict_record_list) - 1)]
    else:
        return {}


def is_need_google_home_lose(user):
    """Google Home の負け処理が必要であるかを返す。

    :param infra.User user: ユーザ
    :rtype: bool
    :return: Google Home の負け処理が必要であるか
    """
    return user.count >= WORDS_COUNT_LIMIT
