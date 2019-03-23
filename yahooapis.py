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

from xml.dom import minidom

import logging

import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

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
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text

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
        xml = api.furigana(sentence)
        dom = minidom.parseString(xml.encode('utf-8'))
        nodes = dom.getElementsByTagName('Furigana')

        hiragana = u''
        for node in nodes:
            hiragana += node.firstChild.data
        logging.info(u'furigana:' + hiragana)

        katakana = replace_hiragana_to_katakana(hiragana)
        logging.info(u'furigana:' + katakana)
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
