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
from xml.dom import minidom

import json
import logging
import random
import urllib

# しりとりが WORDS_COUNT_LIMIT 以上続いたら AI が降参する
WORDS_COUNT_LIMIT = 100

HIRAGANA_TO_KATAKANA = {
    u'ぁ': u'ァ', u'あ': u'ア', u'ぃ': u'ィ', u'い': u'イ', u'ぅ': u'ゥ',
    u'う': u'ウ', u'ぇ': u'ェ', u'え': u'エ', u'ぉ': u'ォ', u'お': u'オ',
    u'か': u'カ', u'が': u'ガ', u'き': u'キ', u'ぎ': u'ギ', u'く': u'ク',
    u'ぐ': u'グ', u'け': u'ケ', u'げ': u'ゲ', u'こ': u'コ', u'ご': u'ゴ',
    u'さ': u'サ', u'ざ': u'ザ', u'し': u'シ', u'じ': u'ジ', u'す': u'ス',
    u'ず': u'ズ', u'せ': u'セ', u'ぜ': u'ゼ', u'そ': u'ソ', u'ぞ': u'ゾ',
    u'た': u'タ', u'だ': u'ダ', u'ち': u'チ', u'ぢ': u'ヂ', u'っ': u'ッ',
    u'つ': u'ツ', u'づ': u'ヅ', u'て': u'テ', u'で': u'デ', u'と': u'ト',
    u'ど': u'ド', u'な': u'ナ', u'に': u'ニ', u'ぬ': u'ヌ', u'ね': u'ネ',
    u'の': u'ノ', u'は': u'ハ', u'ば': u'バ', u'ぱ': u'パ', u'ひ': u'ヒ',
    u'び': u'ビ', u'ぴ': u'ピ', u'ふ': u'フ', u'ぶ': u'ブ', u'ぷ': u'プ',
    u'へ': u'ヘ', u'べ': u'ベ', u'ぺ': u'ペ', u'ほ': u'ホ', u'ぼ': u'ボ',
    u'ぽ': u'ポ', u'ま': u'マ', u'み': u'ミ', u'む': u'ム', u'め': u'メ',
    u'も': u'モ', u'ゃ': u'ャ', u'や': u'ヤ', u'ゅ': u'ュ', u'ゆ': u'ユ',
    u'ょ': u'ョ', u'よ': u'ヨ', u'ら': u'ラ', u'り': u'リ', u'る': u'ル',
    u'れ': u'レ', u'ろ': u'ロ', u'ゎ': u'ヮ', u'わ': u'ワ', u'ゐ': u'ヰ',
    u'ゑ': u'ヱ', u'を': u'ヲ', u'ん': u'ン', u'ゔ': u'ヴ', u'ゕ': u'ヵ',
    u'ゖ': u'ヶ', u'ゝ': u'ヽ', u'ゞ': u'ヾ',
}


def load_dic(json_file_path):
    with open(json_file_path) as json_file:
        json_dic = json.load(json_file)
        json_start_word_dic = json.loads('''
        [{
            "key": "シリトリ",
            "org": ["尻取り"],
            "first": "シ",
            "end": "リ"
        }]''')
        json_dic.extend(json_start_word_dic)
    return json_dic


class User(ndb.Model):
    words = ndb.TextProperty()
    org_words = ndb.TextProperty()
    last_word = ndb.TextProperty()
    last_word_end = ndb.TextProperty()
    count = ndb.IntegerProperty()
    json_file_path = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


def contains_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            return True
    except Exception as e:
        logging.exception(u'contains_user: %s', e)

    return False


def load_user(user_id):
    try:
        user = User.get_by_id(user_id)
        if user:
            user.json_file_path
            return user
    except Exception as e:
        logging.exception(u'load_user: %s', e)

    user = User(id=user_id)
    user.words = u''
    user.org_words = u''
    user.last_word = u''
    user.last_word_end = u''
    user.count = 0
    user.json_file_path = u'data/dict.json'
    word_record = {
        u'key': u'シリトリ',
        u'org': [u'尻取り'],
        u'first': u'シ',
        u'end': u'リ'
    }
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
                   u'org_words': user.org_words,
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
    :param unicode check_word: 検索する単語のrecord
    :rtype: unicode
    :return: 最後に使用した単語に続けられるなら True, 続けられないなら False
    """
    try:
        if check_word[u'first'] == get_last_word_datastore(user):
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
            user.org_words += u',' + save_word_record[u'org'][0]
        else:
            user.words = save_word_record[u'key']
            user.org_words = save_word_record[u'org'][0]
        user.count += 1
    except Exception:
        raise
    user.last_word = save_word_record[u'org'][0]
    user.last_word_end = save_word_record[u'end']
    user.put()


def save_json_file_path(user, json_file_path):
    user.json_file_path = json_file_path
    user.put()


def search_reading_from_dic(search_word, search_word_kana, json_dic):
    """json形式の辞書ファイルを全探索し、引数の文字列を含む単語レコードを返す。

    :param unicode search_word: 検索する文字列
    :param unicode search_word_kana: 検索する文字列のフリガナ
    :param unicode json_dic: json形式の辞書ファイル
    :rtype: unicode
    :return: 検索した単語レコード(辞書にない場合は空の辞書)
    """
    for dict_record in json_dic:
        if dict_record[u'key'] == search_word:
            # search_word が単語の読み仮名と一致
            return dict_record
        for word in dict_record[u'org']:
            if word == search_word:
                # search_word が単語の表記と一致
                return dict_record
        if dict_record[u'key'] == search_word_kana:
            # search_word_kana が単語の読み仮名と一致
            return dict_record
    return {}


def search_word_record_from_dic(user, search_first, json_dic):
    """json形式の辞書ファイルを全探索し、読みが search_first で始まる適当な単語レコードを返す。
    無効な単語（既出の単語・存在しない単語・「ん」で終わる単語）のレコードは返さない。

    :param infra.User user: ユーザ
    :param unicode search_first: カタカナ 1 文字
    :param unicode json_dic: json形式の辞書ファイル
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


def search_lose_word_record_from_dic(user, search_first, json_dic):
    """json形式の辞書ファイルを全探索し、読みが search_first で始まり
    かつ、「ん」で終わる単語レコードを返す。

    :param infra.User user: ユーザ
    :param unicode search_first: カタカナ 1 文字
    :param unicode json_dic: json形式の辞書ファイル
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


class Token(ndb.Model):
    value = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


def load_yahoo_appid():
    try:
        yahoo_appid = Token.get_by_id('yahoo_appid')
        if yahoo_appid and yahoo_appid.value != '!!empty!!':
            return yahoo_appid.value
    except Exception as e:
        logging.exception(u'load_yahoo_appid: %s', e)

    yahoo_appid = Token(id='yahoo_appid')
    yahoo_appid.value = '!!empty!!'
    yahoo_appid.put()
    raise Exception(
        'Set \'yahoo_appid\': https://console.cloud.google.com/datastore/entities;kind=Token')


class YahooFuriganaAPI:
    def __init__(self, appid):
        self.appid = appid

    def _access(self, url, sentence, options={}):
        for key in options:
            if key != 'grade':
                raise KeyError('%s is not acceptable' % (key))
        params = {
            'appid': self.appid,
            'sentence': sentence,
        }
        params.update(options)
        params = urllib.urlencode(params)
        return urllib.urlopen(url, params).read()

    def furigana(self, sentence, options={}):
        xml = self._access(
            'http://jlp.yahooapis.jp/FuriganaService/V1/furigana', sentence, options)
        return xml


def furigana(yahoo_appid, sentence):
    """テキストのフリガナを返却する
    ルビ振り Web API を呼び出し、返却されたふりがなをフリガナに変換する

    :param str yahoo_appid: Yahoo! JAPAN Web API アプリケーション ID
    :param unicode sentence: フリガナを付ける対象のテキスト
    :rtype: unicode
    :return: フリガナ (失敗時は空の文字列)
    """
    try:
        api = YahooFuriganaAPI(yahoo_appid)
        xml = api.furigana(sentence.encode('utf-8'))
        dom = minidom.parseString(xml)
        nodes = dom.getElementsByTagName('Furigana')

        hiragana = u''
        for node in nodes:
            hiragana += node.firstChild.data
        logging.info(hiragana)

        katakana = replace_hiragana_to_katakana(hiragana)
        logging.info(katakana)
        return katakana
    except Exception as e:
        logging.exception(u'furigana: %s', e)
        return u''


def replace_hiragana_to_katakana(hiragana):
    """ひらがな(平仮名)をカタカナ(片仮名)に変換する

    :param unicode hiragana: ひらがなのテキスト
    :rtype: unicode
    :return: カタカナのテキスト
    """
    katakana = hiragana
    for tmp in HIRAGANA_TO_KATAKANA.keys():
        katakana = katakana.replace(tmp, HIRAGANA_TO_KATAKANA[tmp])
    return katakana
