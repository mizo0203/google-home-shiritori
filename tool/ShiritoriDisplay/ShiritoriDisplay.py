# -*- coding: UTF-8 -*-

# Copyright 2018 Hayato Kubo
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

from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.properties import BooleanProperty, StringProperty
from kivy.resources import resource_add_path
from kivy.uix.widget import Widget

import requests

resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, 'ipag.ttf')

# FIXME
URL = 'https://'
PARAMETER = '?id='
ID = ''
REQUEST_URL = URL + PARAMETER + ID

# FIXME: 辞書に応じてオッズを自動取得 or ディスプレイアプリにテキストボックスを追加して起動時に入力
ODDS = 1.2

REQUEST_INTERVAL = 10.0

# 画面下部にて、 1 行で表示できる単語の文字数
LINE_WIDTH = 13


def convertWords2Text(obj):
    org_word_list = obj['org_words'].split(',')
    word_list = obj['words'].split(',')
    out_text = ''
    for i in range(len(word_list)):
        org_word = org_word_list[i]
        word = u'（' + word_list[i] + u'）'
        if len(org_word + word) <= LINE_WIDTH:
            # 単語と読み仮名を合わせて 1 行 (13 文字以下) で表示できる場合
            # 合わせて 1 行で表示する
            lines = [org_word + word]
        else:
            # 単語と読み仮名を合わせて 1 行で表示できない場合
            # 単語と読み仮名を別の行で表示する
            # さらに、それぞれを 13 文字毎に改行する
            lines = [org_word[j:(j + LINE_WIDTH)]
                     for j in range(0, len(org_word), LINE_WIDTH)]
            lines += [word[j:(j + LINE_WIDTH)]
                      for j in range(0, len(word), LINE_WIDTH)]
        if i % 2 == 0:
            tmp = u'AI  :' + lines[0] + u'\n'
        else:
            tmp = u'User:' + lines[0] + u'\n'
        for j in range(1, len(lines), 1):
            tmp += u'     ' + lines[j] + u'\n'
        out_text = tmp + out_text

    return out_text


def omitBy3PointLeader(text, text_len):
    """三点リーダ「…」を使って text を省略する
    """
    if len(text) > text_len:
        text = text[:(text_len - 2)] + u'…' + text[-1]
    return text


class ShiritoriDisplayWidget(Widget):
    is_connect = BooleanProperty()
    word = StringProperty()
    word_end = StringProperty()
    num = StringProperty()
    score = StringProperty()
    word_list = StringProperty()

    def __init__(self, **kwargs):
        super(ShiritoriDisplayWidget, self).__init__(**kwargs)
        self.is_connect = False
        self.word = u'開始待ち'
        self.word_end = u''
        self.num = u'0 回'
        self.score = u'オッズ ' + str(ODDS)
        self.word_list = u''

    def get_JSON(self):
        r = requests.get(REQUEST_URL)
        if r.status_code == 200:
            obj = r.json()
            if obj and self.word != obj['last_word']:
                self.word = omitBy3PointLeader(obj['last_word'], 6)
                self.word_end = obj['last_word_end']
                # 最初の単語 'しりとり' の 1 回分を除外
                num = obj['count'] - 1
                self.num = str(num) + u' 回'
                self.score = '{:.1f}'.format(num * ODDS) + u' 点'
                self.word_list = convertWords2Text(obj)

    def on_command(self, command):
        if command == 'start/stop':
            if self.is_connect:
                self.stop_connect()
            else:
                self.start_connect()
        elif command == 'refresh':
            self.get_JSON()

    def on_timer(self, dt):
        self.get_JSON()

    def start_connect(self):
        self.is_connect = True
        Clock.schedule_interval(self.on_timer, REQUEST_INTERVAL)

    def stop_connect(self):
        self.is_connect = False
        Clock.unschedule(self.on_timer, REQUEST_INTERVAL)


class ShiritoriDisplayApp(App):
    def __init__(self, **kwargs):
        super(ShiritoriDisplayApp, self).__init__(**kwargs)
        self.title = 'ShiritoriDisplay'

    def build(self):
        return ShiritoriDisplayWidget()


if __name__ == '__main__':
    ShiritoriDisplayApp().run()
