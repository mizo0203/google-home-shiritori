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

import utils

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()


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

        katakana = utils.replace_hiragana_to_katakana(hiragana)
        logging.info(u'furigana:' + katakana)
        return katakana
    except Exception as e:
        logging.exception(u'furigana: %s', e)
        return u''
