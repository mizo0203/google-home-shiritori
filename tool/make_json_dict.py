#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

"""
入力ファイルをjsonの辞書ファイルに変換するスクリプト
第一引数:読込ファイル
第二引数:出力ファイル
"""

import argparse
import json
import sys

LOWER_CASE = {u'ァ': u'ア', u'ィ': u'イ', u'ゥ': u'ウ', u'ェ': u'エ', u'ォ': u'オ',
              u'ャ': u'ヤ', u'ュ': u'ユ', u'ョ': u'ヨ', u'ヮ': u'ワ',
              u'ッ': u'ツ',
              }

CONVERSION_TABLE = {u'ヂ': u'ジ', u'ヅ': u'ズ', }

VOICED_SOUND_MARK = {u'ヴ': u'ウ',
                     u'ガ': u'カ', u'ギ': u'キ', u'グ': u'ク', u'ゲ': u'ケ', u'ゴ': u'コ',
                     u'ザ': u'サ', u'ジ': u'シ', u'ズ': u'ス', u'ゼ': u'セ', u'ゾ': u'ソ',
                     u'ダ': u'タ', u'ヂ': u'チ', u'ヅ': u'ツ', u'デ': u'テ', u'ド': u'ト',
                     u'バ': u'ハ', u'ビ': u'ヒ', u'ブ': u'フ', u'ベ': u'ヘ', u'ボ': u'ホ',
                     u'パ': u'ハ', u'ピ': u'ヒ', u'プ': u'フ', u'ペ': u'ヘ', u'ポ': u'ホ',
                     }

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

POKEMON_TABLE = {u'X': u'エックス', u'Y': u'ワイ', u'Z': u'ゼット',
                 u'2': u'ツー',
                 u'♂': u'オス', u'♀': u'メス',
                 }


def hiragana_judge(c):
    if 'ぁ' <= c <= 'ゟ':
        return True
    return False


def katakana_judge(c):
    if '゠' <= c <= 'ヿ':
        return True
    return False


def kana_judge(c):
    if hiragana_judge(c) or katakana_judge(c):
        return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'JSON辞書作成スクリプト')
    parser.add_argument('-b', '--biology', action='store_true', help=u'生物学の学名と和名の対応ファイルの読み込み時に使用')
    parser.add_argument('-n', '--naistdic', action='store_true', help=u'NAIST Japanese Dictionaryの読み込み時に使用')
    parser.add_argument('-p', '--pokemon', action='store_true', help=u'kotofurumiya/pokemon_dataの読み込み時に使用')
    parser.add_argument('inputfile', type=argparse.FileType('r'))
    parser.add_argument('outputfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    with args.inputfile as f:
        inputData = {}
        if args.naistdic:
            for line in f:
                line = line.replace('(', '').replace(')', '').rstrip().split(' ')
                org = line[4]
                keys = line[7].replace('{', '').replace('}', '').split('/')
                for key in keys:
                    if key in inputData:
                        inputData[key].append(org)
                    else:
                        inputData[key] = [org]
        elif args.pokemon:
            obj = json.load(f)
            for record in obj:
                name = record['name']
                yomi = u''
                for v in name:
                    if v in POKEMON_TABLE:
                        yomi += POKEMON_TABLE[v]
                    else:
                        yomi += v
                inputData[yomi] = [name]
        elif args.biology:
            for line in f:
                word = line.rstrip().split('\t')[1]
                if kana_judge(word[0]):
                    if hiragana_judge(word[0]):
                        for tmp in HIRAGANA_TO_KATAKANA.keys():
                            word = word.replace(tmp, HIRAGANA_TO_KATAKANA[tmp])
                    inputData[word.replace(u'・', '').replace(' ', '').replace(u'亜種', u'アシュ')] = [word]
        else:
            sys.exit(u'オプションが指定されていません')
    print('inputData  length:', len(inputData))

    outputData = []
    for key in sorted(inputData.keys()):
        data = {}
        if key == '':
            sys.stderr.write('key is null\n')
            continue
        data['key'] = key
        data['org'] = inputData[key]
        data['first'] = key[0]
        if key[-1] == u'ー':
            if 1 < len(key):
                data['end'] = key[-2]
            else:
                continue
        else:
            data['end'] = key[-1]
        if data['end'] in LOWER_CASE:
            data['end'] = LOWER_CASE[data['end']]
        if data['first'] in CONVERSION_TABLE:
            data['first'] = CONVERSION_TABLE[data['first']]
        if data['end'] in CONVERSION_TABLE:
            data['end'] = CONVERSION_TABLE[data['end']]
        if args.pokemon:
            if data['first'] in VOICED_SOUND_MARK:
                data['first'] = VOICED_SOUND_MARK[data['first']]
            if data['end'] in VOICED_SOUND_MARK:
                data['end'] = VOICED_SOUND_MARK[data['end']]
        for v in key:
            if not katakana_judge(v):
                # print(key)
                break
        else:
            outputData.append(data)
    print('outputData length:', len(outputData))

    with args.outputfile as wf:
        json.dump(outputData, wf, indent=2)
