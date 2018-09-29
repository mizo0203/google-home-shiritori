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
import logging
import random

# しりとりが WORDS_COUNT_LIMIT 以上続いたら AI が降参する
WORDS_COUNT_LIMIT = 10


with open('data/dict.json') as json_file:
    json_dic = json.load(json_file)


class User(ndb.Model):
    words = ndb.TextProperty()
    last_word = ndb.TextProperty()
    last_word_end = ndb.TextProperty()
    count = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


def contains_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            return True
    except Exception as e:
        logging.exception(u'contains_user: %s', e)

    return False


def load_user(user_id, default_last_word=u'シリトリ'):
    try:
        user = User.get_by_id(user_id)
        if user:
            return user
    except Exception as e:
        logging.exception(u'load_user: %s', e)

    user = User(id=user_id)
    user.words = u''
    user.last_word = u''
    user.last_word_end = u''
    user.count = 0
    word_record = search_reading_from_dic(default_last_word)
    save_word_datastore(user, word_record)
    return user


def reset_datastore(user):
    try:
        user.key.delete()
    except Exception as e:
        logging.exception(u'reset_datastore: %s', e)


def get_datastore(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            obj = {u'words': user.words,
                   u'last_word': user.last_word,
                   u'last_word_end': user.last_word_end,
                   u'count': user.count,
                   }
            return obj
    except Exception as e:
        logging.exception(u'get_datasore: %s', e)
    return {}


def get_last_word_datastore(user):
    try:
        return user.last_word_end
    except Exception:
        raise


def check_last_word_datastore(user, check_word):
    """check_word がしりとりで最後に使用した単語に続くかを判定する

    :param infra.User user: ユーザ
    :param unicode check_word: 検索するカタカナの文字列
    :rtype: unicode
    :return: 最後に使用した単語に続けられるなら True, 続けられないなら False
    """
    try:
        if check_word[0] == get_last_word_datastore(user):
            return True
        else:
            return False
    except Exception:
        raise


def check_word_datastore(user, check_word):
    """しりとりで未使用の単語であるかを判定する

    :param infra.User user: ユーザ
    :param unicode check_word: 検索するカタカナの文字列
    :rtype: unicode
    :return: 未使用であれば True, 使用済みであれば False
    """
    try:
        words = user.words.split(u',')
        if check_word in words:
            return False
        else:
            return True
    except Exception:
        raise


def save_word_datastore(user, save_word_record):
    try:
        if user.words:
            user.words += u',' + save_word_record[u'key']
        else:
            user.words = save_word_record[u'key']
        user.count += 1
    except Exception:
        raise
    user.last_word = save_word_record[u'key']
    user.last_word_end = save_word_record[u'end']
    user.put()


def search_reading_from_dic(search_word):
    """json形式の辞書ファイルを全探索し、引数の文字列を含む単語レコードを返す。

    :param unicode search_word: 検索する文字列
    :rtype: unicode
    :return: 検索した単語レコード(辞書にない場合は空の辞書)
    """
    for dict_record in json_dic:
        if dict_record[u'key'] == search_word:
            return dict_record
        for word in dict_record[u'org']:
            if word == search_word:
                return dict_record
    return {}


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
