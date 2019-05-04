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


def replace_hiragana_to_katakana(hiragana):
    """ひらがな(平仮名)をカタカナ(片仮名)に変換する

    :param unicode hiragana: ひらがなのテキスト
    :rtype: unicode
    :return: カタカナのテキスト
    """
    katakana = u''
    for old in hiragana:
        new = HIRAGANA_TO_KATAKANA.get(old)
        if not new:
            katakana += old
        else:
            katakana += new
    return katakana
