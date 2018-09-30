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

REQUEST_INTERVAL = 10.0


def convertWords2Text(words):
    out_text = ''
    word_list = words.split(',')
    for i, v in enumerate(word_list):
        if i % 2 == 0:
            out_text = u'AI  :' + v + u'\n' + out_text
        else:
            out_text = u'User:' + v + u'\n' + out_text
    return out_text


class ShiritoriDisplayWidget(Widget):
    is_connect = BooleanProperty()
    word = StringProperty()
    word_end = StringProperty()
    count = StringProperty()
    word_list = StringProperty()

    def __init__(self, **kwargs):
        super(ShiritoriDisplayWidget, self).__init__(**kwargs)
        self.is_connect = False
        self.word = u'開始待ち'
        self.word_end = u'ち'
        self.count = u'0回目'
        self.word_list = u''

    def get_JSON(self):
        r = requests.get(REQUEST_URL)
        if r.status_code == 200:
            obj = r.json()
            if obj and self.word != obj['last_word']:
                self.word = obj['last_word']
                self.word_end = obj['last_word_end']
                self.count = str(obj['count']) + u'回目'
                self.word_list = convertWords2Text(obj['words'])

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
